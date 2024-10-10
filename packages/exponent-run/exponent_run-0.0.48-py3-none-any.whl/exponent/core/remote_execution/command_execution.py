from pathlib import Path
from typing import Any

from exponent.core.remote_execution import files
from exponent.core.remote_execution.types import (
    CommandRequest,
    CommandResponse,
)
from exponent.core.types.generated.command_request_data import (
    FileReadCommandRequestData,
    PrototypeCommandRequestData,
)


async def execute_command(
    request: CommandRequest,
    working_directory: str,
) -> CommandResponse:
    try:
        match request:
            case CommandRequest(
                correlation_id=correlation_id,
                data=FileReadCommandRequestData(file_path=file_path),
            ):
                path = Path(working_directory, file_path)
                content, _ = await files.get_file_content(path)

                return CommandResponse(
                    content=content,
                    correlation_id=correlation_id,
                )
            case CommandRequest(
                correlation_id=correlation_id,
                data=PrototypeCommandRequestData(
                    command_name=command_name,
                    content_json=content_json,
                    content_raw=content_raw,
                    content_rendered=content_rendered,
                ),
            ):
                content = await execute_prototype_command(
                    command_name=command_name,
                    content_json=content_json,
                    content_raw=content_raw,
                    content_rendered=content_rendered,
                    working_directory=working_directory,
                )

                return CommandResponse(
                    content=content,
                    correlation_id=correlation_id,
                )
            case _:
                raise ValueError(f"Unknown command request: {request}")
    except Exception as e:  # noqa: BLE001 - TODO (Josh): Specialize errors for execution
        return CommandResponse(
            content="An error occurred during command execution: " + str(e),
            correlation_id=request.correlation_id,
        )


async def execute_prototype_command(
    command_name: str,
    content_json: dict[str, Any],
    content_raw: str,
    content_rendered: str,
    working_directory: str,
) -> str:
    if command_name == "file_open":
        return f'Successfully opened file "{content_json["file_path"]}"'
    elif command_name == "search_files":
        results = await files.search_files(
            path_str=content_json["path"],
            file_pattern=content_json["file_pattern"],
            regex=content_json["regex"],
            working_directory=working_directory,
        )
        return "\n".join(results)

    raise ValueError(f"Unhandled prototype command: {command_name}")
