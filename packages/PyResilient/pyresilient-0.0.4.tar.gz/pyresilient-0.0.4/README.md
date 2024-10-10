
# PyResilient

[![PyPI version](https://badge.fury.io/py/PyResilient.svg)](https://pypi.org/project/PyResilient/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PyResilient is a Python module designed to provide resilience strategies such as retries, timeouts, and fallback mechanisms for your functions. This module is ideal for elegantly and robustly handling errors and exceptions in your applications, enhancing reliability and user experience.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Fallback Decorator](#fallback-decorator)
  - [Retry Decorator](#retry-decorator)

- [License](#license)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

## Installation

You can install PyResilient using pip:

```sh
pip install PyResilient
```

*PyResilient requires Python 3.8 or higher.*

## Usage

PyResilient provides decorators that can be easily applied to your functions to add resilience features with minimal code changes.

### Fallback Decorator

The `fallback` decorator allows you to apply a fallback strategy to a function. If the original function raises an exception, the fallback function will be executed.

```python
from PyResilient import fallback

def fallback_function():
    print("Executing fallback function")
    return "Default value"

@fallback(fallback_function, exceptions=(ValueError,))
def my_function():
    raise ValueError("An error occurred")

result = my_function()  # Will print "Executing fallback function"
print(result)  # Outputs: Default value
```

**Parameters:**

- `fallback_function` (*callable*): The function to execute if an exception is raised.
- `exceptions` (*tuple of Exception types*, optional): The exceptions that trigger the fallback. Defaults to `(Exception,)`.

### Retry Decorator

The `retry` decorator allows you to retry the execution of a function a specific number of times before failing.

```python
from PyResilient import retry

@retry(retries=3, exceptions=(ValueError,), delay=2)
def my_function():
    print("Attempting to execute function")
    raise ValueError("An error occurred")

my_function()
# Will attempt to execute the function 3 times with a 2-second delay between attempts
```

**Parameters:**

- `retries` (*int*): The maximum number of retry attempts.
- `exceptions` (*tuple of Exception types*, optional): The exceptions that trigger a retry. Defaults to `(Exception,)`.
- `delay` (*int or float*, optional): The delay between retry attempts in seconds. Defaults to `0`.

### Timeout Decorator

The `timeout` decorator allows you to set a time limit for the execution of a function. If the function does not complete within the specified time, a `TimeoutError` is raised.

```python
from PyResilient import timeout

@timeout(seconds=5)
def my_function():
    import time
    time.sleep(10)
    return "Completed"

try:
    result = my_function()
except TimeoutError:
    print("Function execution timed out")
```

**Parameters:**

- `seconds` (*int or float*): The maximum allowed execution time in seconds.

**Note:** The `timeout` decorator uses threading under the hood, which may have implications for thread safety and resource management in your application.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Author

**Bastián García**

- Email: [bastiang@uc.cl](mailto:bastiang@uc.cl)
- GitHub: [github.com/cve-zh00](https://github.com/cve-zh00)

## Acknowledgments

- Inspired by the need for robust error handling mechanisms in Python applications.
- Thanks to the open-source community for their continuous support and contributions.
