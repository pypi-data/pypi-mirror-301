# ideariver-core

`ideariver-core` is the core library of the ideariver organization, providing essential abstract classes, DTOs, and interfaces for plugins and other services. The package is designed to be lightweight and extensible, making it easy for developers to build upon.

## Usage

The library provides an abstract base class `BasePlugin` for developers to create plugins.

```python
from ideariver_core import BasePlugin

class MyPlugin(BasePlugin):
    def init(self, services):
        # Initialize the plugin with the required services.
        pass

    def run(self, input_data):
        # Process the input data and return the result.
        return "Processed data"
```
