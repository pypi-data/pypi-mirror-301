# COSMIC LOGGER

COSMIC Logger is a Python module designed for logging various types of messages in tools and applications. It provides an easy way to handle debug, error, rate-limit warnings, user input, and informational messages.

## Features

- **Debug Logging**: Log debug messages.
- **Error Logging**: Log error messages.
- **Rate-Limit Logging**: Log rate-limit warnings.
- **User Input Logging**: Log user input.
- **Informational Logging**: Log general informational messages.

## Installation

You can install uwulogger using pip:

```sh
pip install uwulogger
```

## Usage

Here's a quick example of how to use uwulogger:

```python
from COSMIC import log

log.dbg("This is a debug message.")
log.err("This is an error message.")
log.ratelimt("This is a rate-limit warning.")
log.inp("User input received.")
log.inf("This is an informational message.")
```




## License

This project is licensed under the MIT License.
