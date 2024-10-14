# winzy-webcam

[![PyPI](https://img.shields.io/pypi/v/winzy-webcam.svg)](https://pypi.org/project/winzy-webcam/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-webcam?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-webcam/releases)
[![Tests](https://github.com/sukhbinder/winzy-webcam/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-webcam/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-webcam/blob/main/LICENSE)

Take image capture from webcam on laptop

## Installation

First configure your Winzy project [to use Winzy](https://github.com/sukhbinder/winzy).

Then install this plugin in the same environment as your Winzy application.
```bash
pip install winzy-webcam
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-webcam
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
