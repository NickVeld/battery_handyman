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
"""The tests for battery_handyman/util.py"""
import unittest.mock

import psutil
import pytest

import battery_handyman.constants
import battery_handyman.util


def test_get_battery_info():
    """Test that get_battery_info provides the needed data"""
    actual_result = battery_handyman.util.get_battery_info()
    # pylint: disable=no-member
    assert actual_result.is_charging is not None
    assert actual_result.left_in_percents is not None


@pytest.mark.parametrize(
    "mock_value, expected_charging, expected_left_in_percents", [
        pytest.param(
            psutil._common.sbattery(
                percent=98, secsleft=9898, power_plugged=False
            ), False, 98,
        ), pytest.param(
            psutil._common.sbattery(
                percent=42, secsleft=psutil._common.BatteryTime.POWER_TIME_UNLIMITED,
                power_plugged=True
            ), True, 42
        ),
    ]
)
@unittest.mock.patch('psutil.sensors_battery')
# The arg order: mock, from the parametrization, the fixtures
def test_get_battery_info_with_mock(
        mock_psutil_sensors_battery, mock_value, expected_charging, expected_left_in_percents
):
    """Test that get_battery_info process the value from the sensors correctly"""
    mock_psutil_sensors_battery.return_value = mock_value
    actual_result = battery_handyman.util.get_battery_info()
    # pylint: disable=no-member
    assert actual_result.is_charging == expected_charging
    assert actual_result.left_in_percents == expected_left_in_percents


@pytest.mark.parametrize(
    "request_template, expected_result", [
        pytest.param("/power/{needs_charging}", ["needs_charging"]),
        pytest.param("/cm?cmnd=Power%20{needs_charging}", ["needs_charging"]),
    ]
)
def test_parse_request_data_key_list(request_template, expected_result):
    """Test that parse_request_data_key_list parse the provided template correctly"""
    actual_result = battery_handyman.util.parse_request_data_key_list(request_template)
    assert actual_result == expected_result


def test_do_not_toogle_charging_exception():
    """Tests that default DoNotToogleChargingException provides the right message"""
    try:
        raise battery_handyman.util.DoNotToogleChargingException()
    except battery_handyman.util.DoNotToogleChargingException as error:
        assert str(error) == battery_handyman.constants.MSG_CHARGING_MUST_NOT_TO_BE_TOOGLED

    test_message = "Test message"
    try:
        raise battery_handyman.util.DoNotToogleChargingException(test_message)
    except battery_handyman.util.DoNotToogleChargingException as error:
        assert str(error) == test_message
