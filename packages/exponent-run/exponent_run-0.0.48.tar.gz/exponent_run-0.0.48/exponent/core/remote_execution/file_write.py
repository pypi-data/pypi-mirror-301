import logging
import os
import re
import subprocess
from collections.abc import Callable
from textwrap import dedent, indent

from diff_match_patch import diff_match_patch
from pydantic import BaseModel

from exponent.core.remote_execution.types import (
    WRITE_STRATEGY_FULL_FILE_REWRITE,
    WRITE_STRATEGY_NATURAL_EDIT,
    WRITE_STRATEGY_SEARCH_REPLACE,
    WRITE_STRATEGY_UDIFF,
    FileWriteRequest,
    FileWriteResponse,
)
from exponent.core.remote_execution.utils import assert_unreachable

logger = logging.getLogger(__name__)


class FileEditResult(BaseModel):
    content: str | None
    failed_edits: list[tuple[str, str]]


def execute_file_write(
    request: FileWriteRequest, working_directory: str
) -> FileWriteResponse:
    write_strategy = request.write_strategy
    if write_strategy == WRITE_STRATEGY_FULL_FILE_REWRITE:
        result = execute_full_file_rewrite(
            request.file_path, request.content, working_directory
        )
    elif write_strategy == WRITE_STRATEGY_UDIFF:
        result = execute_udiff_edit(
            request.file_path, request.content, working_directory
        )
    elif write_strategy == WRITE_STRATEGY_SEARCH_REPLACE:
        result = execute_search_replace_edit(
            request.file_path, request.content, working_directory
        )
    elif write_strategy == WRITE_STRATEGY_NATURAL_EDIT:
        result = execute_full_file_rewrite(
            request.file_path, request.content, working_directory
        )
    else:
        assert_unreachable(write_strategy)
    return FileWriteResponse(
        content=result,
        correlation_id=request.correlation_id,
    )


def lint_file(file_path: str, working_directory: str) -> str:
    try:
        # Construct the absolute path
        full_file_path = os.path.join(working_directory, file_path)

        # Run ruff check --fix on the file
        result = subprocess.run(
            ["ruff", "check", "--fix", full_file_path],
            capture_output=True,
            text=True,
            check=True,
        )

        # If the subprocess ran successfully, return a success message
        return f"Lint results:\n\n{result.stdout}\n\n{result.stderr}"
    except Exception as e:  # noqa: BLE001
        # For any other errors, return a generic error message
        return f"An error occurred while linting: {e!s}"


def format_results(file_path: str, content: str, working_directory: str) -> str:
    footer = ""

    # In case you want linting
    # if is_editable_install():
    #     lint_result = lint_file(file_path, working_directory)
    #     footer = f"\n\n{lint_result}"

    return content + footer


def execute_full_file_rewrite(
    file_path: str, content: str, working_directory: str
) -> str:
    try:
        # Construct the absolute path
        full_file_path = os.path.join(working_directory, file_path)

        # Check if the directory exists, if not, create it
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        # Determine if the file exists and write the new content
        if os.path.exists(full_file_path):
            with open(full_file_path, "w") as file:
                file.write(content)
            result = f"Modified file {file_path}"
        else:
            with open(full_file_path, "w") as file:
                file.write(content)
            result = f"Created file {file_path}"

        return format_results(file_path, result, working_directory)

    except Exception as e:  # noqa: BLE001
        return f"An error occurred: {e!s}"


def execute_udiff_edit(file_path: str, content: str, working_directory: str) -> str:
    result = execute_partial_edit(file_path, content, working_directory, apply_udiff)
    return format_results(file_path, result, working_directory)


def execute_search_replace_edit(
    file_path: str, content: str, working_directory: str
) -> str:
    result = execute_partial_edit(
        file_path, content, working_directory, apply_all_search_replace
    )
    return format_results(file_path, result, working_directory)


def execute_partial_edit(
    file_path: str,
    edit_content: str,
    working_directory: str,
    edit_function: Callable[[str, str], FileEditResult],
) -> str:
    try:
        # Construct the absolute path
        full_file_path = os.path.join(working_directory, file_path)

        # Check if the directory exists, if not, create it
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        # Determine if the file exists and write the new content
        file_content, created = read_or_init_file(full_file_path)

        success = open_file_and_apply_edit(
            file_path=full_file_path,
            file_content=file_content,
            edit_content=edit_content,
            edit_function=edit_function,
        )

        if success:
            verb = "Created" if created else "Modified"
            return f"{verb} file {file_path}"
        else:
            verb = "create" if created else "modify"
            return f"Failed to {verb} file {file_path}"

    except Exception as e:
        raise e


def read_or_init_file(file_path: str) -> tuple[str, bool]:
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("")
        return "", True

    with open(file_path) as f:
        return f.read(), False


def open_file_and_apply_edit(
    file_path: str,
    file_content: str,
    edit_content: str,
    edit_function: Callable[[str, str], FileEditResult],
) -> bool:
    result = edit_function(file_content, edit_content)

    if not result.content:
        return False

    with open(file_path, "w") as file:
        file.write(result.content)

    return True


def find_leading_whitespace(existing_content: str, search: str) -> str | None:
    existing_lines = existing_content.splitlines()

    search_line_count = len(search.splitlines())
    dedented_search = dedent(search)

    for i in range(len(existing_lines)):
        existing_window_content = "\n".join(existing_lines[i : i + search_line_count])
        dedented_existing_window = dedent(existing_window_content)

        leading_ws_len = len(existing_window_content) - len(
            existing_window_content.lstrip()
        )
        leading_ws = existing_window_content[:leading_ws_len]

        if dedented_existing_window == dedented_search:
            return leading_ws

    return None


def try_fix_whitespace(
    existing_content: str, search: str, replace: str
) -> tuple[str, str] | None:
    # Try to fix the whitespace of the search and replace
    # to make the edit more likely to apply
    leading_ws = find_leading_whitespace(existing_content, search)
    if leading_ws is None:
        return None

    dedented_search = dedent(search)
    dedented_replace = dedent(replace)

    return indent(dedented_search, leading_ws), indent(dedented_replace, leading_ws)


def try_search_replace(existing_content: str, search: str, replace: str) -> str | None:
    # Try simple search and replace first
    new_content = simple_search_and_replace(existing_content, search, replace)
    if new_content:
        print("Applied simple search and replace")
        return new_content

    fixed_ws = try_fix_whitespace(existing_content, search, replace)
    if not fixed_ws:
        return None

    search, replace = fixed_ws

    new_content = simple_search_and_replace(existing_content, search, replace)
    if new_content:
        print("Applied simple search and replace with fixed whitespace")
        return new_content

    return None


def try_diff_patch(existing_content: str, search: str, replace: str) -> str | None:
    new_content = diff_patch_search_and_replace(existing_content, search, replace)
    if new_content:
        print("Applied diff patch search and replace")
        return new_content

    return None


def apply_udiff(existing_content: str, diff_content: str) -> FileEditResult:
    hunks = get_raw_udiff_hunks(diff_content)

    for hunk in hunks:
        if not hunk:
            continue

        search, replace = split_hunk_for_search_and_replace(hunk)

        # Exact match
        new_content = try_search_replace(existing_content, search, replace)
        if new_content is not None:
            print("Applied successfully!")
            return FileEditResult(content=new_content, failed_edits=[])

        # Fuzzy match
        new_content = try_diff_patch(existing_content, search, replace)
        if new_content is not None:
            print("Applied successfully!")
            return FileEditResult(content=new_content, failed_edits=[])

        print("Failed to apply hunk, exiting!")
        return FileEditResult(content=None, failed_edits=[(search, replace)])

    return FileEditResult(content=existing_content, failed_edits=[])


def get_raw_udiff_hunks(content: str) -> list[list[str]]:
    lines = content.splitlines(keepends=True)
    hunks: list[list[str]] = []
    current_hunk: list[str] = []
    for line in lines:
        if line.startswith("@@"):
            if current_hunk:
                hunks.append(current_hunk)
                current_hunk = []
        else:
            current_hunk.append(line)
    if current_hunk:
        hunks.append(current_hunk)
    return hunks


def split_hunk_for_search_and_replace(hunk: list[str]) -> tuple[str, str]:
    search_lines = []
    replace_lines = []

    search_prefixes = ["-", " "]
    replace_prefixes = ["+", " "]
    for line in hunk:
        if not line:
            continue
        prefix, content = line[0], line[1:]
        if not content:
            continue
        if prefix in search_prefixes:
            search_lines.append(content)
        if prefix in replace_prefixes:
            replace_lines.append(content)
    return "".join(search_lines), "".join(replace_lines)


def simple_search_and_replace(content: str, search: str, replace: str) -> str | None:
    if content.count(search) >= 1:
        return content.replace(search, replace)
    return None


def diff_patch_search_and_replace(
    content: str, search: str, replace: str
) -> str | None:
    patcher = diff_match_patch()
    # 3 second tieout for computing diffs
    patcher.Diff_Timeout = 3
    patcher.Match_Threshold = 0.95
    patcher.Match_Distance = 500
    patcher.Match_MaxBits = 128
    patcher.Patch_Margin = 32
    search_vs_replace_diff = patcher.diff_main(search, replace, False)

    # Simplify the diff as much as possible
    patcher.diff_cleanupEfficiency(search_vs_replace_diff)
    patcher.diff_cleanupSemantic(search_vs_replace_diff)

    original_vs_search_diff = patcher.diff_main(search, content)
    new_diffs = patcher.patch_make(search, search_vs_replace_diff)
    # Offset the search vs. replace diffs with the offset
    # of the search diff within the original content.
    for new_diff in new_diffs:
        new_diff.start1 = patcher.diff_xIndex(original_vs_search_diff, new_diff.start1)
        new_diff.start2 = patcher.diff_xIndex(original_vs_search_diff, new_diff.start2)

    new_content, successes = patcher.patch_apply(new_diffs, content)
    if not all(successes):
        return None

    return str(new_content)


SEARCH_REPLACE_RE = re.compile(
    r"[^<>]*<<<+\s*SEARCH\n((?P<search>.*?)\n)??===+\n((?P<replace>.*?)\n)??>>>+\s*?REPLACE\s*?[^<>]*",
    re.DOTALL,
)


def apply_search_replace(result: str, search: str, replace: str) -> str | None:
    if not search and not replace:
        # Nonsense
        return None

    if not search and not result:
        # New file, just return replace
        return replace

    if not search.strip():
        # Search on just whitespace,
        # too dangerous to apply
        return None

    return try_search_replace(result, search, replace)


def apply_all_search_replace(existing_content: str, sr_content: str) -> FileEditResult:
    # Same as apply_search_replace, but applies all search and replace pairs
    # in the sr_content to the existing_content

    result = existing_content
    failed_edits: list[tuple[str, str]] = []

    for match in SEARCH_REPLACE_RE.finditer(sr_content):
        match_dict = match.groupdict()
        search, replace = match_dict.get("search"), match_dict.get("replace")
        search = search or ""
        replace = replace or ""

        new_result = apply_search_replace(result, search, replace)
        if new_result is None:
            failed_edits.append((search, replace))
            continue

        result = new_result

    return FileEditResult(content=result, failed_edits=failed_edits)
