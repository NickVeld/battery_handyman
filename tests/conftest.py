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
"""The configuration of pytest"""
import pytest


def pytest_addoption(parser):
    """The setup of the CLI arguments parsing"""
    parser.addoption(
        "--skip-slow", action="store_true", default=False, help="skip slow tests"
    )


def pytest_configure(config):
    """The initialization of the marks"""
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    """Conditional marking"""
    if not config.getoption("--skip-slow"):
        return
    skip_slow = pytest.mark.skip(reason="remove --skip-slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
