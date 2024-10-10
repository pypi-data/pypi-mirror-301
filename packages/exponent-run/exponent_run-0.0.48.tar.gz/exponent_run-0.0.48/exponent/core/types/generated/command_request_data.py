# Auto-generated, do not edit directly. Run `make generate_command_data` to update.

from enum import Enum
import typing
from typing import Literal

from pydantic import BaseModel


class CommandRequestType(str, Enum):
    FILE_READ = "file_read"
    PROTOTYPE = "prototype"


class CommandRequestData(BaseModel):
    pass


class FileReadCommandRequestData(CommandRequestData):
    type: Literal[CommandRequestType.FILE_READ] = CommandRequestType.FILE_READ

    file_path: str
    language: str


class PrototypeCommandRequestData(CommandRequestData):
    type: Literal[CommandRequestType.PROTOTYPE] = CommandRequestType.PROTOTYPE

    command_name: str
    content_json: dict[str, typing.Any]
    content_raw: str
    content_rendered: str


CommandRequestDataType = FileReadCommandRequestData | PrototypeCommandRequestData
