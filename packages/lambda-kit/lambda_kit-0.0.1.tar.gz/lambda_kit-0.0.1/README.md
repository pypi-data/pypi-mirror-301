# Lambda Kit

Yet another CLI tool for packaging Python Lambda functions and Lambda layers.

## Overview

Whenever I try to create new AWS Lambda functions in Python I always have difficulty packaging the code 
and dependencies. This tool is designed to make it easier to package and deploy Python Lambda functions and Lambda 
layers.

## Installation

```shell
pip install lambda-kit
```

## Usage

Display the help menu:

```bash
lambda-kit --help
```

## Features

- Package Lambda functions
- Package Lambda layers

## Usage

Packaging Lambda Functions

```bash
lambda-kit package --function-name my-function --source-dir /path/to/source --output-dir /path/to/output
```

Packaging Lambda Layers

```bash
lambda-kit package --layer-name my-layer --source-dir /path/to/source --output-dir /path/to/output
```

## References

- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
- [AWS Lambda Deployment Package](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
- [AWS Lambda Layers Deployment Package](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
