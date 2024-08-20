import traceback

from jfw.Logger import Logger

file_path = __file__


class ExceptionHandler:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def handle(self, exception: BaseException) -> None:
        file_name, line_no = self._get_filename_and_line(exception)
        self.logger.log(f'{str(exception)} in {file_name} at line: {line_no}')
        self._print_exception(exception)

    def _print_exception(self, exception: BaseException) -> None:
        file_name, line_no = self._get_filename_and_line(exception)

        print('')
        print(f'Something went wrong. An Exception occurred in {file_name} at line {line_no}')
        print('')
        print(f'{type(Exception)}: {str(exception)}')
        print('')
        print('stacktrace:')
        print('')
        traceback.print_exception(exception)

    def _get_filename_and_line(self, exception):
        file_name = 'an unknown file'
        line_no = 'unknown'
        if exception.__traceback__:
            current_tb_type = exception.__traceback__
            while (current_tb_type.tb_next is not None):
                current_tb_type = current_tb_type.tb_next

            file_name = current_tb_type.tb_frame.f_code.co_filename
            line_no = current_tb_type.tb_frame.f_lineno
        return file_name, line_no

