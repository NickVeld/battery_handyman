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

.. image:: https://raw.githubusercontent.com/NickVeld/battery_handyman/main/docs/assets/battery_handyman_logo.svg
    :target: https://github.com/NickVeld/battery_handyman
    :alt: Logo of Battery Handyman
    :align: right


===============
BatteryHandyman
===============

|pypi| |python| |docs| |license| |test| |codeql| |codefactor| |codecov|

.. |pypi| image:: https://img.shields.io/pypi/v/battery_handyman
    :target: https://pypi.org/project/battery_handyman/
    :alt: PyPI project

.. |python| image:: https://img.shields.io/pypi/pyversions/battery_handyman
    :target: https://pypi.org/project/battery_handyman/
    :alt: Supported Python versions

.. |docs| image:: https://readthedocs.org/projects/battery-handyman/badge/?version=latest
    :target: https://battery-handyman.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |license| image:: https://img.shields.io/github/license/NickVeld/battery_handyman
    :target: https://choosealicense.com/licenses/apache-2.0/
    :alt: License

.. |test| image:: https://github.com/NickVeld/battery_handyman/actions/workflows/python-app.yml/badge.svg
    :target: https://github.com/NickVeld/battery_handyman/actions/workflows/python-app.yml
    :alt: Testing pipeline status

.. |codeql| image:: https://github.com/NickVeld/battery_handyman/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/NickVeld/battery_handyman/actions/workflows/codeql-analysis.yml
    :alt: CodeQL analysis status

.. |codefactor| image:: https://www.codefactor.io/repository/github/NickVeld/battery_handyman/badge
    :target: https://www.codefactor.io/repository/github/NickVeld/battery_handyman
    :alt: Grade from CodeFactor

.. |codecov| image:: https://codecov.io/gh/NickVeld/battery_handyman/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/NickVeld/battery_handyman
    :alt: Code coverage

A customizable battery saving application

----------
Quickstart
----------

See `documentation <https://battery-handyman.readthedocs.io/en/latest/>`_
for more installation and usage ways, the details.

Installation
============

The most simplest way is an installation using ``pip`` from PyPI::

    pip install battery_handyman

Usage
=====

Create a configuration file (for example, ``my_configuration.yml``) and call::

    battery_handyman -c ./my_configuration.yml
