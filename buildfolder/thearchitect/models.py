import json
from pathlib import Path
from typing import List, Sequence

from pydantic import BaseModel, Field


class Variable(BaseModel):
    # TODO provide a specific set of types?
    # HKEY, WSADATA, int, LPHOSTENT, SOCKET, SOCKADDR_IN, struct, char, char*, FILE, long, DWORD
    type: str = Field(
        title='type',
        description='Variable type',
    )
    name: str = Field(
        title='name',
        description='Variable name',
    )
    value: str = Field(
        default=None,
        title='value',
        description='Variable value',
    )


class Piece(BaseModel):
    doc: str = Field(
        default="",
        title='documentation',
        description='Piece documentation',
    )

    headers: Sequence[str] = Field(
        default=[],
        title='headers',
        description='Required headers to include',
    )

    inputs: List[str] = Field(
        default=[],
        title='inputs',
        description='Expected inputs',
    )
    outputs: List[str] = Field(
        default=[],
        title='outputs',
        description='Expected outputs',
    )
    variables: List[Variable] = Field(
        default=[],
        title='variables',
        description='Piece internal variables',
    )

    setupcode: Sequence[str] = Field(
        default=[],
        title='Setup code',
        description='Piece bootstrap code (e.g. structure declaration)',
    )
    corecode: Sequence[str] = Field(
        default=[],
        title='Core code',
        description='Piece core code',
    )
    teardowncode: Sequence[str] = Field(
        default=[],
        title='Teardown code',
        description='Piece post-process code (e.g. variable clean-up)',
    )

    @classmethod
    def from_json(cls, json_path):
        json_path = Path(json_path)
        return cls(**json.load(json_path.open()))
