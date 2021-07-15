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
"""It carries out the tasks on the battery servicing

Now it only sends customizable HTTP requests when the battery
percentage reaches user-defined limits
"""
from __future__ import annotations  # https://stackoverflow.com/a/49872353

import logging
import sched
import time
from argparse import Namespace
from typing import Any, Optional, Dict, Callable

import requests
import yaml  # See the representer and constructor adding in the end of the file

import battery_handyman.constants
import battery_handyman.util


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ConfigSectionNamespace(Namespace):  # pylint: disable=too-few-public-methods
    """A representation of a configuration section

    Defined for the type-checking purposes
    """


def common_property_setter_routine(target_property: Callable) -> Callable:
    """Add logging of the target property and the provided value"""
    def wrapper(self, value):
        target_property(self, value)
        logger.info("%s is set to %s", target_property.__name__, value)

    return wrapper


def common_only_battery_limit_property_setter_routine(target_property: Callable) -> Callable:
    """Adds checking of the provided limit value"""
    def wrapper(self, value):
        if (
                (value < battery_handyman.constants.BATTERY_LIMIT_VALUE_MINIMAL)
                or (value > battery_handyman.constants.BATTERY_LIMIT_VALUE_MAXIMAL)
        ):
            raise ValueError(
                f"The provided limit ({value}) for {target_property.__name__} is invalid"
            )
        target_property(self, value)

    return wrapper


class BatteryHandyman:
    """Central class"""
    def __init__(
            self,
            battery_limit_config: Optional[ConfigSectionNamespace] = None,
            check_config: Optional[ConfigSectionNamespace] = None,
            remote_request_config: Optional[ConfigSectionNamespace] = None,
    ):
        self._skip_send_request = True
        remote_address = None
        request_template = None
        request_data_mapping = None
        if remote_request_config is not None:
            self._skip_send_request = False
            remote_address = remote_request_config.remote_address
            request_template = remote_request_config.request_template
            request_data_mapping = remote_request_config.request_data_mapping
        # Here there is verification that
        # at least one possible reaction to battery check result is registered
        if self._skip_send_request:
            raise TypeError(
                "At least one reaction config is required"
                " Current reaction configs available to set:"
                f" {battery_handyman.constants.CONFIG_NAME_REMOTE_REQUEST}"
            )

        while remote_address.endswith("/"):
            remote_address = remote_address[:-1]

        try:
            self.battery_limit_charged = battery_limit_config.charged
        except AttributeError:
            self.battery_limit_charged = battery_handyman.constants.BATTERY_LIMIT_VALUE_DEFAULT_CHARGED
        try:
            self.battery_limit_low = battery_limit_config.low
        except AttributeError:
            self.battery_limit_low = battery_handyman.constants.BATTERY_LIMIT_VALUE_DEFAULT_LOW

        try:
            self.check_interval = check_config.check_interval
        except AttributeError:
            self.check_interval = battery_handyman.constants.CHECK_INTERVAL_IN_SECONDS_DEFAULT

        self.remote_address = remote_address
        self.request_template = request_template
        self.request_method = remote_request_config.request_method
        self.request_data_mapping = request_data_mapping

        self._scheduler = sched.scheduler(time.time, time.sleep)

    # SECTION: IO
    @classmethod
    def from_configuration_file(cls, configuration_filepath: str) -> BatteryHandyman:
        """Creates an instance using the file path pointing at the configuration file"""
        with open(configuration_filepath, mode='r') as configuration_file:
            load_result = yaml.safe_load(configuration_file)
        if load_result is None:
            raise ValueError("Most probably the configuration file is empty")
        if isinstance(load_result, BatteryHandyman):
            return load_result
        instance = BatteryHandyman.__new__(BatteryHandyman)
        instance.init_from_config_dict_mapping(load_result)
        return instance

    def to_configuration_file(self, configuration_filepath: str) -> None:
        """Creates the configuration file under the provided file path"""
        with open(configuration_filepath, mode='w') as configuration_file:
            yaml.safe_dump(self, configuration_file)

    def init_from_config_dict_mapping(self, config_dict_mapping: Dict[str, Dict[str, Any]]) -> None:
        """Initializes the instance using a configuration dictionary"""
        try:
            config_namespaces_mapping = {
                config_section_name: ConfigSectionNamespace(**config)
                for config_section_name, config in config_dict_mapping.items()
            }
            self.__init__(**config_namespaces_mapping)
        except (TypeError, ValueError, AttributeError):
            aux_exception = ValueError(
                "Something is wrong with the selected configuration file."
                " Please, compare its structure and the default one"
            )
            # How to get rid of the traceback here?
            # Ways with redefining the "sys" module things from
            # https://stackoverflow.com/questions/38598740/raising-errors-without-traceback
            # disable traceback for the caught exception too.
            # raise aux_exception.with_traceback(TracebackType(None, EMPTY_FRAME, 0, 0))
            # does not work too because the way to create empty traceback correctly is unknown
            raise aux_exception

    def to_config_dict_mapping(self) -> Dict[str, Dict[str, Any]]:
        """Creates a configuration dictionary from the instance"""
        config_dict_mapping = {
            battery_handyman.constants.CONFIG_NAME_BATTERY_LIMIT: {
                "charged": self.battery_limit_charged,
                "low": self.battery_limit_low,
            },
            battery_handyman.constants.CONFIG_NAME_CHECK: {
                "check_interval": self.check_interval,
            },
        }

        if not self._skip_send_request:
            config_dict_mapping[battery_handyman.constants.CONFIG_NAME_REMOTE_REQUEST] = {
                "remote_address": self.remote_address,
                "request_data_mapping": self.request_data_mapping,
                "request_method": self.request_method,
                "request_template": self.request_template,
            }
        return config_dict_mapping

    # SUBSECTION: PyYAML SUPPORT
    YAML_TAG = "!BatteryHandyman"

    @staticmethod
    def to_yaml(dumper: yaml.SafeDumper, data: BatteryHandyman) -> yaml.MappingNode:
        """A YAML dumping function"""
        return dumper.represent_mapping(data.YAML_TAG, data.to_config_dict_mapping())

    @staticmethod
    def from_yaml(loader: yaml.SafeLoader, node: Any) -> BatteryHandyman:
        """A YAML loading function

        See also https://stackoverflow.com/a/49458752
        """
        instance = BatteryHandyman.__new__(BatteryHandyman)
        yield instance
        node_map = loader.construct_mapping(node, deep=True)
        instance.init_from_config_dict_mapping(node_map)  # pylint: disable=protected-access

    # SECTION: REQUESTER
    def extract_request_data(
            self, battery_info: battery_handyman.util.BatteryInfo
    ) -> Dict[str, Any]:
        """Transforms `battery_info` into the dictionary of the data
         requited by the request line template"""
        request_data = {}
        request_data_key_needs_charging = battery_handyman.constants.REQUEST_DATA_KEY_NEEDS_CHARGING
        if request_data_key_needs_charging in self._request_data_key_list:
            if battery_info.is_charging:
                if battery_info.left_in_percents > self.battery_limit_charged:
                    logger.debug("Charging must be disabled")
                    request_data[request_data_key_needs_charging] = False
            else:
                if battery_info.left_in_percents < self.battery_limit_low:
                    logger.debug("Charging must be enabled")
                    request_data[request_data_key_needs_charging] = True
            if request_data_key_needs_charging not in request_data:
                logger.debug(battery_handyman.constants.MSG_CHARGING_MUST_NOT_TO_BE_TOOGLED)
                raise battery_handyman.util.DoNotToogleChargingException
        return request_data

    def map_request_data_inplace(self, request_data: Dict[str, Any]) -> None:
        """Maps the values extracted from `battery_info` to the specified in the configuration"""
        for request_arg, value in request_data.items():
            if request_arg in self.request_data_mapping:
                request_arg_value_mapping = self.request_data_mapping[request_arg]
                if value in request_arg_value_mapping:
                    request_data[request_arg] = request_arg_value_mapping[value]

    def send_request(self, battery_info: battery_handyman.util.BatteryInfo) -> None:
        """Runs the whole pipeline from processing `battery_info` to HTTP response handling"""
        if self._skip_send_request:
            return

        request_data = self.extract_request_data(battery_info)
        self.map_request_data_inplace(request_data)
        ready_request_line = (
            self.remote_address + self.request_template.format(**request_data)
        )

        logger.info("Sending %s request to %s", self.request_method, ready_request_line)

        # Retry will be performed after the next check if it is needed
        try:
            response = requests.request(self.request_method, ready_request_line)
        except requests.exceptions.ConnectionError as exception_instance:
            logger.error(
                "%s request to %s: %s",
                self.request_method, ready_request_line, exception_instance
            )
            return

        if response.status_code <= battery_handyman.constants.RESPONSE_STATUS_CODE_SUCCESS_MAX:
            logger.debug(
                "Response %s to %s request to %s", response.status_code,
                self.request_method, ready_request_line
            )
            return

        logger.error(
            "Response %s to %s request to %s. Reason: %s", response.status_code,
            self.request_method, ready_request_line, response.reason
        )

    # SECTION: CHECKER
    def perform_check(self) -> None:
        """Obtains `battery_info`, pass it to `send_request` and schedule the next check"""
        battery_info = battery_handyman.util.get_battery_info()
        try:
            self.send_request(battery_info)
        except battery_handyman.util.DoNotToogleChargingException:
            pass
        self.schedule_new_check()

    def schedule_new_check(self, initial: bool = False) -> None:
        """Only adds additional entry in the scheduler"""
        self._scheduler.enter(
            0 if initial else self.check_interval, 1, self.perform_check
        )

    def start(self, blocking: bool = True) -> None:
        """Runs the check cycle"""
        self.schedule_new_check(initial=True)
        self._scheduler.run(blocking=blocking)

    def stop(self) -> None:
        """Stops the check cycle"""
        if not self._scheduler.empty():
            for event in self._scheduler.queue:
                self._scheduler.cancel(event)

    # SECTION: PROPERTIES
    @property
    def battery_limit_charged(self) -> int:
        """A threshold. A battery is considered as charged
         if its percentage is greater than the threshold"""
        return self._battery_limit_charged

    @battery_limit_charged.setter
    @common_property_setter_routine
    @common_only_battery_limit_property_setter_routine
    def battery_limit_charged(self, value: int) -> None:
        self._battery_limit_charged = value

    @property
    def battery_limit_low(self) -> int:
        """A threshold. A battery is considered as low enough to charge
         if its percentage is less than the threshold"""
        return self._battery_limit_low

    @battery_limit_low.setter
    @common_property_setter_routine
    @common_only_battery_limit_property_setter_routine
    def battery_limit_low(self, value: int) -> None:
        self._battery_limit_low = value

    @property
    def check_interval(self) -> int:
        """A time interval between checks in seconds"""
        return self._check_interval

    @check_interval.setter
    @common_property_setter_routine
    def check_interval(self, value: int) -> None:
        self._check_interval = value

    @property
    def remote_address(self) -> str:
        """The address of the remote device that controls the charging of this device"""
        return self._remote_address

    @remote_address.setter
    @common_property_setter_routine
    def remote_address(self, value: str) -> None:
        self._remote_address = value

    @property
    def request_template(self) -> str:
        """A URL path template with named placeholders"""
        return self._request_template

    @request_template.setter
    @common_property_setter_routine
    def request_template(self, value: str) -> None:
        self._request_data_key_list = None
        if value:
            self._request_data_key_list = battery_handyman.util.parse_request_data_key_list(value)

        self._request_template = value

    @property
    def request_method(self) -> str:
        """A HTTP method of the requests"""
        return self._request_method

    @request_method.setter
    @common_property_setter_routine
    def request_method(self, value: str) -> None:
        self._request_method = value

    @property
    def request_data_mapping(self) -> Dict[Any, Any]:
        """A mapping for the values prepared for `request_template`"""
        return self._request_data_mapping

    @request_data_mapping.setter
    @common_property_setter_routine
    def request_data_mapping(self, value: Dict[Any, Any]) -> None:
        self._request_data_mapping = value


yaml.add_representer(BatteryHandyman, BatteryHandyman.to_yaml, Dumper=yaml.SafeDumper)
yaml.add_constructor(
    BatteryHandyman.YAML_TAG, BatteryHandyman.from_yaml, Loader=yaml.SafeLoader
)
