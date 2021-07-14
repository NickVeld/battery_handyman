.. ..
    Copyright [2021] [Nikolay Veld]
    _
    Licensed under the Apache License, Version 2.0 \(the "License"\);
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    _
        http://www.apache.org/licenses/LICENSE-2.0
    _
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

===============
BatteryHandyman
===============

A customizable battery saving application

-------
General
-------

The software carries out the tasks on the battery servicing

Now it only sends customizable HTTP requests when the battery
percentage reaches user-defined limits

---------------------------------------
Comparison with the similar application
---------------------------------------

+-----------------------+-------------------+--------------------+
| Feature/quality       | *BatteryHandyman* | Battery Limiter\*  |
+=======================+===================+====================+
| Notifications         | In plans          | \+                 |
+-----------------------+-------------------+--------------------+
| | HTTP requests       | \+                | | Not working\**,  |
| | to smart devices    |                   | | not flexible\*** |
+-----------------------+-------------------+--------------------+
| GUI                   | In plans          | \+                 |
+-----------------------+-------------------+--------------------+
| Open-source           | \+                | \-                 |
+-----------------------+-------------------+--------------------+
| Portable Installation | \+                | \-                 |
+-----------------------+-------------------+--------------------+
    \* The version: 1.0.7

    \** The test mode works but the application sends nothing when the limit achived

    \*** Only one URL for the all limits

-----
Usage
-----

First of all, download the application.

Configuration file
=================

The usage of the templates is encouraged.
They are located in the `configurations` directory.

Only one reaction configuration section is required.
The currently supported reaction configuration sections:

* ``remote_request_config``

The content of the `default_configuration.yml`::

    !BatteryHandyman
    battery_limit_config:
      charged: 90
      low: 40
    check_config:
      # In seconds
      check_interval: 1
    remote_request_config:
      remote_address: http://127.0.0.1:80
      request_method: POST
      request_template: /power/{needs_charging}
      request_data_mapping:
        needs_charging:
          True: 1
          False: 0

Reference
---------

* ``!BatteryHandyman``
  -- allows creating the instance from the file using PyYAML directly

* ``battery_limit_config``
  -- the configuration section that set the battery limits
  (used as thresholds for certain actions)

* ``check_config``
  -- the configuration section that set the battery checking up

  - ``check_interval`` -- an integer values meaning the period in seconds between

* ``remote_request_config``
  -- the configuration section that provided the details needed for the requests

  - ``remote_address`` -- the address of the remote device
    (scheme, host address, port)
  - ``request_method`` -- the HTTP method to be permoformed sending a request
  - ``request_template`` -- the path part of the URL with a named template placeholder(s)
  - ``request_data_mapping`` -- it maps a value from a default value range to a needed one.


Command Line Interface
======================

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_PATH, --config-path CONFIG_PATH
                        The path to the configuration YAML file relative to
                        the "configuration" directory (default:
                        default_configuration.yml)

The basic command-to-run list is the following one
assuming you have ``my_configuration.yml``
in ``/path/to/battery_handyman/repo/root/configurations/``
(skip the ``cd`` command if you have installed the module
or have the module in ``PYTHONPATH``)::

    cd /path/to/battery_handyman/repo/root
    python -m battery_handyman -c my_configuration.yml

Or the app can be called with the following command
if you have Python's "scripts" directory in the path::

    battery_handyman -c ./my_configuration.yml

Using import
============

You can use ``BatteryHandyman`` in another Python application.

First of all, ensure that you have installed the package,
have the package in ``PYTHONPATH``
or the ``battery_handyman``
(one that have the ``.py`` files inside in the top-level)
and ``configuration`` directories in the directory with the importing script.
(There are advanced options for placing and importing Python packages)

Then::

    import battery_handyman

    battery_handyman.main(["-c", "my_configuration.yml"])

In case you want to use the class directly,
in the first place see through the details of `main` carefully.