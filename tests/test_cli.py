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
"""The tests for battery_handyman/cli.py"""
from argparse import Namespace

import pytest

import battery_handyman.cli


@pytest.mark.parametrize(
    "cli_args, expected_result", [
        pytest.param([], Namespace(config_path="default_configuration.yml")),
        pytest.param(["--config-path", "absent.yml"], Namespace(config_path="absent.yml")),
    ]
)
def test_setup_parser(cli_args, expected_result):
    """Test only argument parsing"""
    parser = battery_handyman.cli.setup_parser()
    actual_result = parser.parse_args(cli_args)
    assert actual_result == expected_result
