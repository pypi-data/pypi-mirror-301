# Strig

[![GitHub releases](https://img.shields.io/github/v/release/w-kuipers/strig)](https://github.com/w-kuipers/strig/releases)
[![PyPI release](https://img.shields.io/pypi/v/strig.svg)](https://pypi.org/project/strig/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/github/last-commit/w-kuipers/strig?label=last%20modified)](https://github.com/w-kuipers/strig)
[![Tests](https://github.com/w-kuipers/strig/actions/workflows/tests.yml/badge.svg)](https://github.com/w-kuipers/strig/actions/workflows/tests.yml)

Strig is an open-source Python utility package for generating random strings and numbers. It is lightweight, flexible, and perfect for use in application backends where unique IDs, secure passwords, or bulk test data are needed.

## Features

- Generate random **alphanumeric**, **alphabetic**, or **numeric** strings.
- Customize length, prefixes, and casing options.
- Verify uniqueness against a database.

## Installation

### Install using PIP

    pip install strig

Note that `pip` refers to the Python 3 package manager. In an environment where Python 2 is also present the correct command may be `pip3`.

## Usage

Strig can be used to create unique identifiers, test data, or even secure passwords. The simple and customizable functions allow you to specify the format that fits your needs.
For detailed documentation and additional functionality, visit the [full documentation](https://strig.w-kuipers.com/).

### Import strig:

```python copy
import strig
```

### Generate an alphanumeric string

Generate a 6-character long string composed of letters and numbers.

```python copy
random_alphanumeric = strig.alphanumeric()
print(random_alphanumeric)  # Example output: 'A3c9Dz'
```

### Generate an alphabetic string

Generate a 10-character long string composed of lower-case letters only.

```python copy
random_alpha = strig.alpha(length=10, case="lower")
print(random_alpha)  # Example output: 'abcdefghij'
```

### Generate an numeric value

Generate an 8-digit long integer and prefix it with _12_. The total number of digits will be 10.

```python copy
random_numeric = strig.numeric(length=8, prefix=12)
print(random_numeric)  # Example output: 1297637456
```

## Support

If you come across any issues, please [create an issue](https://github.com/w-kuipers/strig/issues) on GitHub.

## License

Strig is licensed under the [MIT License](https://github.com/w-kuipers/strig/blob/master/LICENSE)
