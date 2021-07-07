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
"""The setup of the CLI arguments parsing"""
import argparse


def setup_parser() -> argparse.ArgumentParser:
    """Return the parser of the CLI arguments"""
    parser = argparse.ArgumentParser(
        prog="battery_handyman",
        description=(
            "Checks battery status periodically"
            " and react to it according to the provided configuration"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-c", "--config-path", default="default_configuration.yml", help=(
            "The path to the configuration YAML file"
            " relative to the \"configuration\" directory"
        )
    )
    return parser
