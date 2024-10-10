# Format-Logger

Format Logger allows you to have a nice looking log, with relevant information as function and time, and calculate the elapsed time during the functions, with a easy to use structure. 

## Install

```
pip install format-logger
```

## Example

```
from format_logger.logger import logger

def foo_function(log : logger) -> None:
    log = log.start_function("foo_function")

    log.INFO("Hello World!")
    time.sleep(1)

    log.end_function()

if __name__ == "__main__":

    log = logger("logger_example", "main")

    foo_function(log)

    log.end_function()
```
Output: 

logger_example | main | 2024-10-09 17:19:18.563839 | INFO | Starting function main at 2024-10-09 17:19:18.563839

logger_example | foo_function | 2024-10-09 17:19:18.563839 | INFO | Starting function foo_function at 2024-10-09 17:19:18.563839

logger_example | foo_function | 2024-10-09 17:19:18.563839 | INFO | Hello World!

logger_example | foo_function | 2024-10-09 17:19:19.564759 | INFO | Function foo_function ended - time 1.00092 Seconds

logger_example | main | 2024-10-09 17:19:19.564759 | INFO | Function main ended - time 1.00092 Seconds
