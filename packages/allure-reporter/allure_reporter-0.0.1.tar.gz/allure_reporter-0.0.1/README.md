# Readme

This is CLI tool for handling Allure reports, mainly targeting the docker builds released by [fescobar](https://github.com/fescobar), but should work with other setups of Allure Report. If using something else than fescobar docker images, make sure you set the environment variable `ALLURE_API_ENDPOINT` to the correct endpoint for the api calls.

## Usage



## Environment variables

Many options could be replaced with environment variables.

| Environment Variable | Description             | Default |
| -------------------- | ----------------------  | ------- |
| `ALLURE_RESULTS_DIRECTORY` | Path to directory with Allure results  | `allure-results` |
| `ALLURE_SERVER` | Allure server address | - |
| `ALLURE_PROJECT_ID` | Allure project | `default` |
| `ALLURE_USER` | Allure user to login with | - |
| `ALLURE_PASSWORD` | Allure password to login with | - |
| `ALLURE_SSL_VERIFICATION` | Enable or disable SSL verification | `true` |
| `ALLURE_API_ENDPOINT` | Which URL to construct path to the api | `allure-docker-service` |
| `ALLURE_FORCE_PROJECT_CREATION` | If project should be created if it doesn't exist | `true` |

## License

Copyright (C) 2024 Digitalist Open Cloud <cloud@digitalist.com>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
