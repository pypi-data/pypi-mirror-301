"""CLI tool for handling Allure Reports."""

import os
import base64
import json
import logging
from pathlib import Path
import requests
import click

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ENDPOINT = os.getenv("ALLURE_API_ENDPOINT", "allure-docker-service")
api_endpoint = API_ENDPOINT

FORCE_PROJECT_CREATION = os.getenv("ALLURE_FORCE_PROJECT_CREATION", "true")
force_project_creation = FORCE_PROJECT_CREATION


def prepare_results_files(results_directory):
    """preparing files."""
    # Get the current working directory
    current_directory = Path.cwd()
    logger.info("Path we are looking for files in: %s", current_directory)
    results_directory_path = os.path.join(current_directory, results_directory)
    if not os.path.exists(results_directory_path):
        logger.error("Directory does not exist: %s", results_directory_path)
        return []
    files = os.listdir(results_directory_path)
    results = []

    logger.info("Files in directory:")
    for file in files:
        result = {}
        file_path = os.path.join(results_directory, file)

        logger.info(file_path)

        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
                if content.strip():
                    b64_content = base64.b64encode(content)
                    result["file_name"] = file
                    result["content_base64"] = b64_content.decode("UTF-8")
                    results.append(result)
                else:
                    logger.warning("Empty file skipped: %s", {file_path})
        else:
            logger.warning("Directory skipped: %s", {file_path})

    return results


def login_to_allure(allure_server, user, password, ssl_verification):
    """helper function for login."""
    headers = {"Content-type": "application/json"}
    credentials_body = {"username": user, "password": password}
    json_credentials_body = json.dumps(credentials_body)

    logger.debug("Logging in")
    session = requests.Session()
    response = session.post(
        f"{allure_server}/{api_endpoint}/login",
        headers=headers,
        data=json_credentials_body,
        verify=ssl_verification,
    )

    logger.debug("Status code: %s", {response.status_code})

    if response.status_code == 200:
        csrf_access_token = session.cookies.get("csrf_access_token")
        if csrf_access_token:
            logger.debug("CSRF-ACCESS-TOKEN: %s", {csrf_access_token})
            return session, csrf_access_token
        else:
            raise Exception("CSRF access token not found in login response")
    else:
        raise Exception(
            f"Login failed with status code {response.status_code}: {response.content}"
        )


def api_request(session, method, url, headers=None, data=None, verify=True):
    """Helper function for making API requests."""
    logger.info("Making %s request to %s", {method}, {url})
    try:
        response = session.request(
            method, url, headers=headers, data=data, verify=verify
        )
        response.raise_for_status()  # Raises an exception for 4XX/5XX responses
        return response
    except requests.RequestException as e:
        logger.error("API request failed: %s", {e})
        raise


# Sending results
@click.command()
@click.option(
    "--allure-results-directory",
    required=True,
    envvar="ALLURE_RESULTS_DIRECTORY",
    default="allure-results",
    help="Path to allure results directory.",
)
@click.option(
    "--allure-server", required=True, envvar="ALLURE_SERVER", help="Allure server URL."
)
@click.option(
    "--project-id", required=True, envvar="ALLURE_PROJECT_ID", help="Allure project ID."
)
@click.option("--user", required=True, envvar="ALLURE_USER", help="Allure username.")
@click.option(
    "--password", required=True, envvar="ALLURE_PASSWORD", help="Allure password."
)
@click.option(
    "--ssl-verification",
    default=True,
    envvar="ALLURE_SSL_VERIFICATION",
    help="Enable or disable SSL verification.",
)
def send_results(
    allure_results_directory,
    allure_server,
    project_id,
    user,
    password,
    ssl_verification,
):
    """
    Send results.
    """
    current_directory = os.path.dirname(os.path.realpath(__file__))
    results_directory = os.path.join(current_directory, allure_results_directory)
    logger.debug("Results directory path: %s", {results_directory})

    # Prepare files
    results = prepare_results_files(results_directory)

    # Login and get session with CSRF token
    session, csrf_access_token = login_to_allure(
        allure_server, user, password, ssl_verification
    )

    # Prepare and send results
    logger.info("Send results")
    headers = {"Content-type": "application/json", "X-CSRF-TOKEN": csrf_access_token}
    request_body = {"results": results}
    json_request_body = json.dumps(request_body)

    url = f"{allure_server}/{API_ENDPOINT}/send-results?project_id={project_id}&force_project_creation={force_project_creation}"
    response = api_request(
        session,
        "POST",
        url,
        headers=headers,
        data=json_request_body,
        verify=ssl_verification,
    )

    logger.debug("Status code: %s", {response.status_code})
    logger.debug("Response")

    json_response_body = json.loads(response.content)
    json_dump = json.dumps(json_response_body, indent=4, sort_keys=True)
    logger.info(json_dump)


# Generate report
@click.command()
@click.option(
    "--allure-server", required=True, envvar="ALLURE_SERVER", help="Allure server URL."
)
@click.option(
    "--project-id", required=True, envvar="ALLURE_PROJECT_ID", help="Allure project ID."
)
@click.option("--user", required=True, envvar="ALLURE_USER", help="Allure username.")
@click.option(
    "--password", required=True, envvar="ALLURE_PASSWORD", help="Allure password."
)
@click.option(
    "--ssl-verification",
    default=True,
    envvar="ALLURE_SSL_VERIFICATION",
    help="Enable or disable SSL verification.",
)
@click.option("--execution-name", required=True, help="Execution name for the report.")
@click.option(
    "--execution-from", required=True, help="Execution source (URL or identifier)."
)
@click.option(
    "--execution-type",
    default="ci",
    help="Execution type (e.g., gitlab, jenkins, etc.).",
)
def generate_report(
    allure_server,
    project_id,
    execution_name,
    execution_from,
    execution_type,
    user,
    password,
    ssl_verification,
):
    """
    Generate report.
    """
    session, csrf_access_token = login_to_allure(
        allure_server, user, password, ssl_verification
    )

    logger.info("Generate report")
    headers = {"X-CSRF-TOKEN": csrf_access_token}

    response = session.get(
        f"{allure_server}/{api_endpoint}/generate-report?project_id={project_id}"
        f"&execution_name={execution_name}&execution_from={execution_from}&execution_type={execution_type}",
        headers=headers,
        verify=ssl_verification,
    )

    logger.debug("Status code: %s", {response.status_code})

    if response.status_code == 200:
        json_response_body = json.loads(response.content)
        json_dump = json.dumps(json_response_body, indent=4, sort_keys=True)

        logger.info(json_dump)
        logger.info("Allure report URL: %s", {json_response_body["data"]["report_url"]})

    else:
        logger.error(
            "Failed to generate report. Status code: %s", {response.status_code}
        )


# Get projects
@click.command()
@click.option(
    "--allure-server", required=True, envvar="ALLURE_SERVER", help="Allure server URL."
)
@click.option("--user", required=True, envvar="ALLURE_USER", help="Allure username.")
@click.option(
    "--password", required=True, envvar="ALLURE_PASSWORD", help="Allure password."
)
@click.option(
    "--ssl-verification", default=True, help="Enable or disable SSL verification."
)
def get_projects(allure_server, user, password, ssl_verification):
    """
    Get projects.
    """
    session, csrf_access_token = login_to_allure(
        allure_server, user, password, ssl_verification
    )
    headers = {"Content-type": "application/json", "X-CSRF-TOKEN": csrf_access_token}
    response = session.get(
        f"{allure_server}/{api_endpoint}/projects",
        headers=headers,
        verify=ssl_verification,
    )

    logger.debug("Status code: %s", {response.status_code})

    json_response_body = json.loads(response.content)
    json_dump = json.dumps(json_response_body, indent=4, sort_keys=True)
    logger.info(json_dump)


# Get config
@click.command()
@click.option(
    "--allure-server", required=True, envvar="ALLURE_SERVER", help="Allure server URL."
)
@click.option("--user", required=True, envvar="ALLURE_USER", help="Allure username.")
@click.option(
    "--password", required=True, envvar="ALLURE_PASSWORD", help="Allure password."
)
@click.option(
    "--ssl-verification", default=True, help="Enable or disable SSL verification."
)
def get_config(allure_server, user, password, ssl_verification):
    """
    Get config.
    """
    session, csrf_access_token = login_to_allure(
        allure_server, user, password, ssl_verification
    )
    headers = {"Content-type": "application/json", "X-CSRF-TOKEN": csrf_access_token}
    response = session.get(
        f"{allure_server}/{api_endpoint}/config",
        headers=headers,
        verify=ssl_verification,
    )

    logger.debug("Status code: %s", {response.status_code})

    json_response_body = json.loads(response.content)
    json_dump = json.dumps(json_response_body, indent=4, sort_keys=True)
    logger.info(json_dump)


# Create project
@click.command()
@click.option(
    "--allure-server", required=True, envvar="ALLURE_SERVER", help="Allure server URL."
)
@click.option("--user", required=True, envvar="ALLURE_USER", help="Allure username.")
@click.option(
    "--password", required=True, envvar="ALLURE_PASSWORD", help="Allure password."
)
@click.option(
    "--project-id", required=True, envvar="ALLURE_PROJECT_ID", help="Allure project ID."
)
@click.option(
    "--ssl-verification", default=True, help="Enable or disable SSL verification."
)
def create_project(allure_server, user, password, project_id, ssl_verification):
    """
    Create project
    """
    session, csrf_access_token = login_to_allure(
        allure_server, user, password, ssl_verification
    )
    headers = {"Content-type": "application/json", "X-CSRF-TOKEN": csrf_access_token}
    payload = {"id": project_id}
    json_payload = json.dumps(payload)
    response = session.post(
        f"{allure_server}/{api_endpoint}/projects",
        headers=headers,
        data=json_payload,
        verify=ssl_verification,
    )

    logger.debug("Status code: %s", {response.status_code})
    logger.debug("Response:")
    json_response_body = json.loads(response.content)

    logger.info({json_response_body["meta_data"]["message"]})

    json_dump = json.dumps(json_response_body, indent=4, sort_keys=True)
    logger.debug(json_dump)


# Delete project
@click.command()
@click.option(
    "--allure-server", required=True, envvar="ALLURE_SERVER", help="Allure server URL."
)
@click.option("--user", required=True, envvar="ALLURE_USER", help="Allure username.")
@click.option(
    "--password", required=True, envvar="ALLURE_PASSWORD", help="Allure password."
)
@click.option(
    "--project-id", required=True, envvar="ALLURE_PROJECT_ID", help="Allure project ID."
)
@click.option(
    "--ssl-verification", default=True, help="Enable or disable SSL verification."
)
def delete_project(allure_server, user, password, project_id, ssl_verification):
    """
    Delete project
    """
    session, csrf_access_token = login_to_allure(
        allure_server, user, password, ssl_verification
    )
    headers = {"Content-type": "application/json", "X-CSRF-TOKEN": csrf_access_token}

    response = session.delete(
        f"{allure_server}/{api_endpoint}/projects/{project_id}",
        headers=headers,
        verify=ssl_verification,
    )

    logger.debug("Status code: %s", {response.status_code})
    logger.debug("Response:")
    json_response_body = json.loads(response.content)
    json_dump = json.dumps(json_response_body, indent=4, sort_keys=True)
    logger.info(json_dump)


@click.group()
def cli():
    """
    Define cli
    """


cli.add_command(send_results)
cli.add_command(generate_report)
cli.add_command(get_config)
cli.add_command(get_projects)
cli.add_command(create_project)
cli.add_command(delete_project)

if __name__ == "__main__":
    cli()
