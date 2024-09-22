from typing import TypedDict

from app.dto.meta import Meta as MetaDto
from app.dto.init import Init as InitDto


class Game(TypedDict):
    meta: MetaDto
    state: dict
    init: InitDto
