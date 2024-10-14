[![Tests](https://github.com/relative-finance/sdk_v2/actions/workflows/test.yml/badge.svg)](https://github.com/relative-finance/sdk_v2/actions/workflows/test.yml) [![Deploy](https://github.com/relative-finance/sdk_v2/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/relative-finance/sdk_v2/actions/workflows/deploy.yml)

# RFX Python SDK

A Python-based SDK developed for interacting with RFX Exchange, offering tools and scripts for executing various operations, including trading and liquidity management.

## Table of Contents
- [Usage](#usage)
- [Local Installation](#local-installation)
- [Running Tests](#running-tests)

## Usage
The SDK can be installed via pip:
```sh
pip install pyrfx
```

## Local Installation
The supported Python versions: >= 3.10 <4

To set up the SDK locally, follow these steps:
```sh
mkdir dist/
cd ./dist
poetry build
cd ..
poetry install --with dev
```

## Running Tests
To execute tests:
```sh
poetry run pytest
```

