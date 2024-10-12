# The Hop Test

At Hop Labs we strive to write high quality software. It's not easy to measure
this empirically but we can measure some proximate signals for quality. That is
what this tool is trying to achieve. We want to measure every thing we can about
a code repository that is suggestive of high quality code.

For now we only support python projects.

## Installation

You can install as a precommit hook:

```yaml
# .pre-commit-hooks.yaml
repos:
-   repo: https://github.com/hopservices/the-hop-test
    rev: v0.1.2
    hooks:
    -   id: the-hop-test
```

You can install with pip from PyPI:

```shell
pip install the-hop-test
```

## Usage

Run the script in the root of your repository

```shell
hoptest
```

## Configuration

By default, the `hoptest` will read configuration settings from
`./hoptest.toml`, but you can specify where the file is with

```shell
hoptest --config path/to/hoptest.toml
```

An example config file looks like

```toml
# ./hoptest.toml
[tool.hoptest]
license_file = "custom-license.txt"
skip_checks = ["logging"]
```

## Development

To build and publish to PyPI, run the following

```shell
rye build
rye publish --skip-existing
```
