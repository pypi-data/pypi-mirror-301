from format_logger.logger import logger
import time

def foo_function(log : logger) -> None:
    log = log.start_function("foo_function")

    log.INFO("Hello World!")
    time.sleep(1)

    log.end_function()

if __name__ == "__main__":

    log = logger("logger_example", "main")

    foo_function(log)

    log.end_function()
