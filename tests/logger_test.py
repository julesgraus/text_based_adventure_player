from time import strptime
from unittest.mock import patch, mock_open, Mock, MagicMock
import unittest

from jfw.Logger import Logger

class LoggerTestCase(unittest.TestCase):
    def test_it_logs(self):
        log_path_mock = MagicMock()
        log_path_mock.__str__.return_value = 'test_log_dir'

        config_mock = Mock()
        config_mock.log_path = Mock(return_value=log_path_mock)

        fixed_time = strptime('2024-01-19 02:11:14', '%Y-%m-%d %H:%M:%S')

        with (
            patch("jfw.Logger.localtime", Mock(return_value=fixed_time)) as localtime_mock,
            patch("builtins.open", mock_open()) as mock_file,
        ):
            logger = Logger(
                config=config_mock,
                log_name='test'
            )

            logger.log(message='Test Message')
            mock_file.assert_called_once_with('test_log_dir/test.log', 'at+', encoding='utf-8')
            handle = mock_file()
            handle.write.assert_called_once_with('[2024-01-19 02:11:14] Test Message\n')
            handle.close.assert_called_once()




