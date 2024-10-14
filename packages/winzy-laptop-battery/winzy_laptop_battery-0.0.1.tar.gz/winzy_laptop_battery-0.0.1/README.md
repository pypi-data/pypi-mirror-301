# winzy-laptop-battery

[![PyPI](https://img.shields.io/pypi/v/winzy-laptop-battery.svg)](https://pypi.org/project/winzy-laptop-battery/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-laptop-battery?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-laptop-battery/releases)
[![Tests](https://github.com/sukhbinder/winzy-laptop-battery/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-laptop-battery/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-laptop-battery/blob/main/LICENSE)

Get laptop battery info and warn if asked

## Installation

First configure your Winzy project [to use Winzy](https://github.com/sukhbinder/winzy).

Then install this plugin in the same environment as your Winzy application.
```bash
pip install winzy-laptop-battery
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-laptop-battery
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
