<h1 style="text-align: center">
    <strong>logger uuid</strong>
</h1>
<p style="text-align: center">
    <a href="https://github.com/anddyagudelo/logger-uuid" target="_blank">
        <img src="https://img.shields.io/github/last-commit/anddyagudelo/logger-uuid" alt="Latest Commit">
    </a>
    <a href="https://pypi.org/project/logger-uuid" target="_blank">
        <img src="https://img.shields.io/pypi/v/logger-uuid" alt="Package version">
    </a>
</p>

This project was created with the purpose of adding a unique identifier to the logs.

## Installation

``` bash
pip install logger-uuid
```

## Usage

```python
from logger_uuid import Logger

class Test:
    def __init__(self, logger: Logger):
        self.logger = logger

    async def get_test(self):    
        self.logger.log_info("log info example")
        self.logger.log_warning("log warning example")
        ...
```