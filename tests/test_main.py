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
"""The tests for battery_handyman/main.py"""
import os.path
import multiprocessing
import subprocess
import time

import pytest

import battery_handyman


@pytest.mark.slow
@pytest.mark.parametrize(
    "cli_args, no_error_is_expected", [
        pytest.param([], True, id="default_cli_args"),
        pytest.param(
            ["--config-path", "template_configuration_tasmota.yml"], True, id="another_config"
        ),
        pytest.param(["--config-path", "absent.yml"], False, id="absent_config"),
    ]
)
def test_main_using_import(cli_args, no_error_is_expected):
    """Test runability like when someone imports this package"""
    path_to_dir_with_main_module = os.path.dirname(battery_handyman.__file__)
    app_process = multiprocessing.Process(
        target=battery_handyman.main,
        args=(cli_args,),
        kwargs={"path_to_dir_with_main_module": path_to_dir_with_main_module},
        name="battery_handyman"
    )
    try:
        app_process.start()
        time.sleep(3)
        assert app_process.is_alive() == no_error_is_expected, \
            "The exit code of the process -- " + str(app_process.exitcode)
    finally:
        if app_process.is_alive():
            app_process.terminate()
            app_process.join(timeout=2)
            try:
                assert not(app_process.exitcode is None), \
                    "The process is still alive even after the termination signal"
            finally:
                app_process.close()
        else:
            # `return` cannot be used in the `finally`
            app_process.close()


@pytest.mark.slow
@pytest.mark.parametrize(
    "cli_args", [
        pytest.param([], id="default_cli_args"),
    ]
)
def test_main_using_import_in_testing_mode(cli_args):
    """Other tests in this module does not affect the coverage of the main"""
    path_to_dir_with_main_module = os.path.dirname(battery_handyman.__file__)
    battery_handyman.main(
        cli_args, path_to_dir_with_main_module=path_to_dir_with_main_module, testing=True
    )


@pytest.mark.slow
@pytest.mark.parametrize(
    "cli_args", [
        pytest.param([], id="default_cli_args"),
        pytest.param(["--config-path", "template_configuration_tasmota.yml"], id="another_config"),
    ]
)
def test_main_using_subprocess(cli_args):
    """Test runability like when someone uses a shell"""
    bh_process = subprocess.Popen(["python", "--version"], stdout=subprocess.PIPE)
    return_code = bh_process.wait()
    assert return_code == 0, "\"python\" cannot be found in directories in PATH"
    python_version = bh_process.stdout.readline()
    assert python_version.startswith("Python 3".encode("utf-8"))

    bh_process = subprocess.Popen(
        ["python", "-m", "battery_handyman"] + cli_args,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    time.sleep(2.5)
    return_code = bh_process.poll()
    if return_code is None:
        # Expected behavior, no error has occurred
        bh_process.terminate()
        bh_process.wait(timeout=2)
        return
    # Unexpected behavior, most probably the process has finished because of an error
    print("Stdout:", bh_process.stdout.read().decode("utf-8"), sep="\n")
    print("Stderr:", bh_process.stderr.read().decode("utf-8"), sep="\n")
    # assert return_code == 0
    raise AssertionError("The process has finished too early")
