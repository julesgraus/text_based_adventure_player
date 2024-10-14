from typing import TypedDict
from app.dto.system_data import SystemData as SystemDataDto

class State(TypedDict):
    game_data_checksum: str
    system_data_checksum: str
    game_data: dict
    system_data: SystemDataDto
