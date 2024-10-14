from typing import TypedDict

from app.dto.meta import Meta as MetaDto
from app.dto.init import Init as InitDto
from app.dto.state import State as StateDto


class Game(TypedDict):
    meta: MetaDto
    state: StateDto
    init: InitDto
