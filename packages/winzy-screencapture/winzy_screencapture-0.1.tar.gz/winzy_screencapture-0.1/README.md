# winzy-screencapture

[![PyPI](https://img.shields.io/pypi/v/winzy-screencapture.svg)](https://pypi.org/project/winzy-screencapture/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-screencapture?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-screencapture/releases)
[![Tests](https://github.com/sukhbinder/winzy-screencapture/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-screencapture/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-screencapture/blob/main/LICENSE)

Capture screen using movieio

## Installation

First configure your Winzy project [to use Winzy](https://github.com/sukhbinder/winzy).

Then install this plugin in the same environment as your Winzy application.
```bash
pip install winzy-screencapture
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-screencapture
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
