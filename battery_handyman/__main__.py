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
"""The entrypoint of the module"""

import os.path
import sys

from .main import main


# pylint: disable=invalid-name
argv = sys.argv
path_to_dir_of_this_module = os.path.dirname(argv[0])
main(argv[1:], path_to_dir_with_main_module=path_to_dir_of_this_module)
