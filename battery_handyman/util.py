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
"""Auxiliary package-level definitions"""
from typing import List, NamedTuple

import psutil

import battery_handyman.constants


class BatteryInfo(NamedTuple):
    """A package-level representation of a battery state"""
    is_charging: bool
    left_in_percents: int


def get_battery_info() -> BatteryInfo:
    """Return a namespace with the `is_charging` and `left_in_percents` key-values"""
    battery_info = psutil.sensors_battery()
    is_charging = battery_info.power_plugged
    left_in_percents = battery_info.percent
    return BatteryInfo(
        is_charging=is_charging,
        left_in_percents=left_in_percents,
    )


def parse_request_data_key_list(request_template: str) -> List[str]:
    """Extract the names of the placeholders in the request line template"""
    request_data_key_list = battery_handyman.constants.TEMPLATE_REGEXP.findall(request_template)
    request_data_key_list = [
        key for key in request_data_key_list
        if key in battery_handyman.constants.REQUEST_DATA_VALID_KEY_LIST
    ]
    return request_data_key_list


class DoNotToogleChargingException(Exception):
    """Signals that the charging process must be unchanged"""
    __doc__ += battery_handyman.constants.MSG_CHARGING_MUST_NOT_TO_BE_TOOGLED

    def __init__(self, *args, **kwargs):
        if not args:
            args = (battery_handyman.constants.MSG_CHARGING_MUST_NOT_TO_BE_TOOGLED, )
        super().__init__(*args, **kwargs)
