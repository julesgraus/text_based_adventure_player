import unittest
from unittest.mock import Mock

from jfw.kernel import Kernel


class TestKernel(unittest.TestCase):
    def test_it_calls_the_callback(self):
        kernel = Kernel(exception_handler=Mock())
        main = Mock()

        kernel.handle(main)
        main.assert_called_once()

    def test_it_calls_the_exception_handler_when_callback_throws_exception(self):
        exception_handler = Mock()

        exception = RuntimeError('Test')

        kernel = Kernel(exception_handler=exception_handler)
        main = Mock(side_effect=exception)

        kernel.handle(main)
        main.assert_called_once()
        exception_handler.handle.assert_called_once_with(exception)

    def test_it_does_not_call_the_exception_handler_when_the_exception_is_a_keyboard_interrupt(self):
        exception_handler = Mock()

        exception = KeyboardInterrupt()

        kernel = Kernel(exception_handler=exception_handler)
        main = Mock(side_effect=exception)

        kernel.handle(main)
        main.assert_called_once()
        exception_handler.handle.assert_not_called()
