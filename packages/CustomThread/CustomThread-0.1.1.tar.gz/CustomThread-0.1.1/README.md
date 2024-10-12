# CustomThread

## Introduction

`CustomThread` is a custom threading class in Python that extends the functionality of the standard `threading.Thread` class. It provides additional features such as returning the result of the target function, raising exceptions in the thread, and more control over the thread lifecycle.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation

Para instalar o `CustomThread` via `pip`, execute:

```bash
pip install CustomThread
```

Depois, você pode importar e usar a classe `CustomThread` em seu projeto:

```python
from customThread import CustomThread
```

Certifique-se de ter o Python 3.x instalado. Para mais detalhes, visite a [página do PyPI](https://pypi.org/project/CustomThread/).

## Usage

```python
from customThread import CustomThread

def example_function(param1, param2):
    print(f"Parameters are {param1} and {param2}")
    return param1 + param2

# Create a CustomThread instance
thread = CustomThread(target=example_function, args=(5, 10))

# Start the thread
thread.start()

# Join the thread and get the return value
result = thread.join()
print(f"Result from thread: {result}")
```

## Features

- **Return Value**: The thread can return a value from the target function, which can be accessed by calling the `join` method.
- **Exception Handling**: Allows raising exceptions in the thread using the `raise_exception` method.
- **Thread Identification**: Provides a method to get the thread ID with `get_id`.
- **Stop Event**: Uses a threading event to indicate when the thread should stop.
- **Daemon Thread Support**: Can be set as a daemon thread during initialization.

## Dependencies

- Python 3.x
- `ctypes` module (included in the standard library)

## Configuration

No specific configuration is required. The class can be directly used by creating instances of `CustomThread`.

## Documentation

### Class: `CustomThread`

#### `__init__(self, group=None, target=None, name=None, args=(), kwargs={}, daemon=None, verbose=None)`
Initializes a new `CustomThread` instance.

- **group**: Thread group (default is `None`).
- **target**: Target function to call when the thread starts.
- **name**: Thread name (default is `None`).
- **args**: Arguments to pass to the target function (default is an empty tuple).
- **kwargs**: Keyword arguments to pass to the target function (default is an empty dictionary).
- **daemon**: If `True`, the thread will run as a daemon (default is `None`).
- **verbose**: Verbosity level (not used in the current implementation).

#### `run(self)`
Executes the target function with the given arguments and keyword arguments, storing the return value.

#### `join(self, *args, **kwargs)`
Waits for the thread to finish and returns the result of the target function.

#### `get_id(self)`
Returns the ID of the respective thread.

#### `raise_exception(self)`
Raises a `SystemExit` exception in the thread to stop its execution. If the exception cannot be raised, an error message will be printed.

## Examples

See the [Usage](#usage) section for a basic example.

## Troubleshooting

- **Exception Raise Failure**: If raising an exception in the thread fails, an error message will be printed. Make sure the thread is running when trying to raise an exception.
- **Return Value**: Ensure the target function returns a value if you intend to capture it using the `join` method.

## Contributors

- [LeoGotardo](https://github.com/LeoGotardo)

## License

This project is licensed under the MIT License.

---
