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
"""The tests for battery_handyman/battery_handyman_class.py"""
import filecmp
import os.path
import random
import re
import tempfile
import time
import unittest.mock
from argparse import Namespace
from contextlib import ExitStack as DoesNotRaise

import pytest
import requests.exceptions
import yaml

from battery_handyman.util import DoNotToogleChargingException
from battery_handyman.battery_handyman_class import (
    BatteryHandyman,
    common_only_battery_limit_property_setter_routine,
)


CONFIG_DIR = "configurations"
CONFIG_PATH_DEFAULT = os.path.join(CONFIG_DIR, "default_configuration.yml")


def test_common_only_battery_limit_property_setter_routine():
    """Tests the handling of the incorrect battery limit"""
    def dummy_method(self, arg):
        # Suppress "unused argument" warning
        _ = self
        return arg

    decorated_dummy_method = common_only_battery_limit_property_setter_routine(dummy_method)
    with pytest.raises(ValueError, match=re.compile(r"\(101\) for dummy_method")):
        decorated_dummy_method(None, 101)


@pytest.fixture(name="default_battery_handyman_instance")
def default_battery_handyman_instance_fixture():
    """The instance created from the default configuration file"""
    battery_handyman_instance = BatteryHandyman.from_configuration_file(CONFIG_PATH_DEFAULT)
    return battery_handyman_instance


@pytest.mark.parametrize(
    "battery_info, expected_url_path, expectation, http_response", [
        pytest.param(
            Namespace(is_charging=False, left_in_percents=1),
            "/power/1",
            DoesNotRaise(),
            (200, "OK"),
            id="discharged",
        ),
        pytest.param(
            Namespace(is_charging=True, left_in_percents=1),
            None,
            pytest.raises(DoNotToogleChargingException),
            (200, "OK"),
            id="charging"
        ),
        pytest.param(
            Namespace(is_charging=True, left_in_percents=100),
            "/power/0",
            DoesNotRaise(),
            (200, "OK"),
            id="charged"
        ),
        pytest.param(
            Namespace(is_charging=False, left_in_percents=100),
            None,
            pytest.raises(DoNotToogleChargingException),
            (200, "OK"),
            id="discharging"
        ),
        pytest.param(
            Namespace(is_charging=False, left_in_percents=1),
            "/power/1",
            DoesNotRaise(),
            (404, "Not Found"),
            id="remote_not_found",
        ),
        pytest.param(
            Namespace(is_charging=False, left_in_percents=1),
            "/power/1",
            DoesNotRaise(),
            (-1, "ConnectionError"),
            id="remote_connection_error",
        ),
    ]
)
@unittest.mock.patch('requests.request')
# The arg order: mock, from the parametrization, the fixtures
def test_send_request_with_mock(
        requests_request_mock,
        battery_info, expected_url_path, expectation, http_response,
        default_battery_handyman_instance,
):
    """Tests ability to send HTTP requests"""
    if http_response[0] == -1:
        requests_request_mock.side_effect = requests.exceptions.ConnectionError()
    else:
        requests_request_mock.return_value = unittest.mock.Mock(
            status_code=http_response[0], reason=http_response[1],
        )
    with expectation:
        default_battery_handyman_instance.send_request(battery_info)
    if expected_url_path is None:
        requests_request_mock.assert_not_called()
        return
    requests_request_mock.assert_called_once_with(
        default_battery_handyman_instance.request_method,
        default_battery_handyman_instance.remote_address + expected_url_path,
    )


@pytest.mark.parametrize(
    "config_path", [
        pytest.param(CONFIG_PATH_DEFAULT, id="default_config")
    ]
)
def test_battery_handyman_load_and_dump(config_path):
    """Tests that the instance from the loaded configuration can be dumped properly

    Checks the contents of the target configuration file and the dumped one will be the same
    """
    battery_handyman_instance = BatteryHandyman.from_configuration_file(config_path)

    # I need a path not a file descriptor so there is no tempfile.TemporaryFile
    dump_path = os.path.join(
        tempfile.gettempdir(),
        tempfile.gettempprefix() + hex(random.randint(2 ** 8, 2 ** 9)) + ".yml"
    )

    battery_handyman_instance.to_configuration_file(dump_path)

    filecmp.clear_cache()
    if not filecmp.cmp(config_path, dump_path, shallow=False):
        with open(config_path) as config_file:
            config_header = config_file.readline()
            config_content = yaml.safe_load(config_file)
        with open(dump_path) as dump_file:
            dump_header = dump_file.readline()
            dump_content = yaml.safe_load(dump_file)

        assert dump_header == config_header
        assert dump_content == config_content


@pytest.mark.slow
@pytest.mark.parametrize(
    "config_path, test_check_interval", [
        pytest.param(CONFIG_PATH_DEFAULT, 1, id="default_config")
    ]
)
def test_battery_handyman_runability(config_path, test_check_interval):
    """Tests the instance of the BatterHandyman starts and finishes properly"""
    battery_handyman_instance = BatteryHandyman.from_configuration_file(config_path)
    battery_handyman_instance.check_interval = test_check_interval

    try:
        battery_handyman_instance.start(blocking=False)
        time.sleep(test_check_interval * 2.5)
    finally:
        battery_handyman_instance.stop()
