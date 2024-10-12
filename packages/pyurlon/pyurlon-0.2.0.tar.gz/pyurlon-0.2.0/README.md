# pyurlon

[![CI - Main](https://github.com/adamws/pyurlon/actions/workflows/main.yml/badge.svg)](https://github.com/adamws/pyurlon/actions/workflows/main.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/pyurlon.svg)](https://pypi.org/project/pyurlon)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyurlon.svg)](https://pypi.org/project/pyurlon)
[![Coverage Status](https://coveralls.io/repos/github/adamws/pyurlon/badge.svg?branch=master)](https://coveralls.io/github/adamws/pyurlon?branch=master)

-----

This is python port of [urlon](https://github.com/cerebral/urlon) javascript package.
It is compatible with urlon version 3.1.0.

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install pyurlon
```

## Usage

```python
>>> import pyurlon
>>> pyurlon.stringify({"table":{"achievement":{"column":"instance","ascending":True}}})
'$table$achievement$column=instance&ascending:true'
>>> pyurlon.parse("$table$achievement$column=instance&ascending:true")
{'table': {'achievement': {'column': 'instance', 'ascending': True}}}
```

## License

`pyurlon` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
