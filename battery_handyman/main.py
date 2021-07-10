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
"""Top-level commands"""
import os.path
import time

import battery_handyman.cli
from battery_handyman.battery_handyman_class import BatteryHandyman


def main(args, path_to_dir_with_main_module: str = "battery_handyman", testing: bool = False):
    """The entrypoint of the application

    With testing == False this function can not be covered
    """
    cli_parser = battery_handyman.cli.setup_parser()
    parsed_args = cli_parser.parse_args(args)
    config_dir = os.path.join(
        path_to_dir_with_main_module, "..", "configurations"
    )
    real_config_path = os.path.join(config_dir, parsed_args.config_path)
    battery_handyman_instance = BatteryHandyman.from_configuration_file(real_config_path)
    try:
        battery_handyman_instance.start(blocking=not(testing))
        if testing:
            time.sleep(2.5)
    finally:
        battery_handyman_instance.stop()
