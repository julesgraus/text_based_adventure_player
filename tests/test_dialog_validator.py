import unittest
from unittest.mock import patch

from app.dialog_validator import DialogValidator
from app.game_creator import GameCreator
from app.game_loader import GameLoader
from app.game_player import GamePlayer
from jfw.config import Config
from jfw.container import Container
from tests.helpers.GameTestHelper import GameTestHelper


class TestDialogValidator(unittest.TestCase):
    def test_it_prints_validation_errors_for_empty_dialog(self) -> None:
        output_string = self._validate_dialog_that_has_content_content(
            dialog_name="test_dialog",
            dialog_file_contents={}
        )
        self.assertIn('text is required', output_string)
        self.assertIn('actions is required', output_string)

    def test_it_prints_validation_errors_for_dialog_with_empty_or_invalid_values(self) -> None:
        output_string = self._validate_dialog_that_has_content_content(
            dialog_name="test_dialog",
            dialog_file_contents={
                "text": "",
                "actions": {}
            }
        )
        self.assertIn('text is required', output_string)
        self.assertIn('text must be longer than 1', output_string)
        self.assertIn('text must end with .txt', output_string)
        self.assertIn('actions is required', output_string)
        self.assertIn('actions must be a list', output_string)
        self.assertIn('actions must be longer than 1', output_string)

    def test_it_prints_validation_errors_for_invalid_action_dict_value(self) -> None:
        output_string = self._validate_dialog_that_has_content_content(
            dialog_name="test_dialog",
            dialog_file_contents={
                "actions": {1}
            }
        )

        self.assertIn('action must be a string', output_string)

    def _validate_dialog_that_has_content_content(self, dialog_name: str, dialog_file_contents: dict) -> str:
        config = Config('')
        game_test_helper = GameTestHelper(config)
        game_test_helper.setup_empty_temp_base_game_path()

        dialog_validator = DialogValidator(config=config)

        with (
            patch("builtins.print", return_value="") as mock_output,
        ):
            game_test_helper.create_dialog(
                game_name="test",
                dialog_name=dialog_name,
                dialog_file_contents=dialog_file_contents,
                txt_file_contents=""
            )

            errors = dialog_validator.validate('test', 'test_dialog').get_errors()

            # the mock output are Text class instances which can be converted to strings.
            return "".join(errors)

if __name__ == '__main__':
    unittest.main()
