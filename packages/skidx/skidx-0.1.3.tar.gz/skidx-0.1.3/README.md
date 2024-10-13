# loda logger 

loda Logger is a Python module designed for logging various types of messages in tools and applications. It provides an easy way to handle debug, error, rate-limit warnings, user input, and informational messages.

## Features

- **Debug Logging**: Log debug messages.
- **Error Logging**: Log error messages.
- **Rate-Limit Logging**: Log rate-limit warnings.
- **User Input Logging**: Log user input.
- **Informational Logging**: Log general informational messages.

## Installation

You can install skidx using pip:

```sh
pip install skidx
```

## Usage

Here's a quick example of how to use lodaLogged:

```python
from COSMIC import loda

loda.dbg("This is a debug message.")
loda.err("This is an error message.")
loda.ratelimt("This is a rate-limit warning.")
loda.inp("User input received.")
loda.inf("This is an informational message.")
```




## License

This project is licensed under the MIT License.
