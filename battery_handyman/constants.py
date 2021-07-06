#    Copyright [2021] [Nikolay Veld]
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Package-level constants"""
import re


# Thing (placed in the 1st group) between curly brackets
TEMPLATE_REGEXP = re.compile(r"\{([^}]+)\}")

BATTERY_INFO_KEY_IS_CHARGING = "is_charging"
BATTERY_INFO_KEY_LEFT_INPERCENTS = "left_in_percents"

BATTERY_LIMIT_VALUE_MINIMAL = 0
BATTERY_LIMIT_VALUE_MAXIMAL = 100
BATTERY_LIMIT_VALUE_DEFAULT_CHARGED = 90
BATTERY_LIMIT_VALUE_DEFAULT_LOW = 40

CONFIG_NAME_BATTERY_LIMIT = "battery_limit_config"
CONFIG_NAME_CHECK = "check_config"
CONFIG_NAME_REMOTE_REQUEST = "remote_request_config"

MSG_CHARGING_MUST_NOT_TO_BE_TOOGLED = "Charging must not to be toogled"

RESPONSE_STATUS_CODE_SUCCESS_MAX = 399

REQUEST_DATA_KEY_NEEDS_CHARGING = "needs_charging"
REQUEST_DATA_VALID_KEY_LIST = [REQUEST_DATA_KEY_NEEDS_CHARGING, ]
