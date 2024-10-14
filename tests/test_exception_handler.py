import sys
import io
import unittest
from unittest.mock import Mock

from jfw.exception_handler import ExceptionHandler


class TestExceptionHandler(unittest.TestCase):
    def test_it_calls_the_loggers_log_method_to_log_the_exception_and_prints_the_exception(self):
        logger_mock = Mock()
        exception_handler = ExceptionHandler(logger_mock)

        saved_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            exception_handler.handle(RuntimeError('A test error'))
        except RuntimeError:
            pass

        printed_data = sys.stdout.getvalue()
        sys.stdout = saved_stdout

        logger_mock.log.assert_called_with('A test error in an unknown file at line: unknown')

        self.assertTrue('Something went wrong. An Exception occurred in' in printed_data)
        self.assertTrue('A test error' in printed_data)
        self.assertTrue('stacktrace:' in printed_data)
