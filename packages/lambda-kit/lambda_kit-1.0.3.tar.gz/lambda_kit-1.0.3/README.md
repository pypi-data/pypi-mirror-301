# Lambda Packager

A CLI tool for packaging and deploying Python Lambda functions and Lambda layers.

## Overview

Whenever I try to create new AWS Lambda functions in Python I always have difficulty packaging the code 
and dependencies. This tool is designed to make it easier to package and deploy Python Lambda functions and Lambda 
layers.

## Installation

Setup a virtual environment:

```shell
python3 -m venv venv
```

Source the virtual environment:

```shell
source venv/bin/activate
```

Upgrade pip:

```shell
pip install --upgrade pip
```

Install the package:

```bash
pip install .
```

Install the package in editable mode:

```bash
pip install -e .
```





Note: This assumes you have defined a pyproject.toml file with the necessary dependencies.



## Usage

```bash
lambda-packager --help
```

## Features

- Package Lambda functions
- Package Lambda layers
- Deploy Lambda functions
- Deploy Lambda layers


## Usage

### Packaging Lambda Functions

```bash
lambda-packager package --function-name my-function --source-dir /path/to/source --output-dir /path/to/output
```

### Packaging Lambda Layers

```bash
lambda-packager package --layer-name my-layer --source-dir /path/to/source --output-dir /path/to/output
```

## References

- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
- [AWS Lambda Deployment Package](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
- [AWS Lambda Layers Deployment Package](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
