from dataclasses import dataclass
from importlib.resources import files
from typing import Dict, Any, List, Union, Callable, Optional

from unmanic.libs.unplugins.settings import PluginSettings

_LIBRARY_ID = "subs_not_ass"


@dataclass
class Issue:
    """A new issue that will show up as an error in the UI"""

    id: str
    message: str


@dataclass
class OnLibraryManagementFileTestData:
    """
    The 'data' object argument includes:
        library_id                      - The library that the current task is associated with
        path                            - String containing the full path to the file being tested.
        issues                          - List of currently found issues for not processing the file.
        add_file_to_pending_tasks       - Boolean, is the file currently marked to be added to the queue for processing.
        priority_score                  - Integer, an additional score that can be added to set the position of the new task in the task queue.
        shared_info                     - Dictionary, information provided by previous plugin runners. This can be appended to for subsequent runners.
    """

    library_id: str
    path: str
    issues: List[Issue]
    add_file_to_pending_tasks: bool
    priority_score: int
    shared_info: Dict[str, Any]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "library_id": self.library_id,
            "path": self.path,
            "issues": self.issues,
            "add_file_to_pending_tasks": self.add_file_to_pending_tasks,
            "priority_score": self.priority_score,
            "shared_info": self.shared_info,
        }


def on_library_management_file_test_make_from_dict(
    d: Dict[str, Any]
) -> OnLibraryManagementFileTestData:
    return OnLibraryManagementFileTestData(
        library_id=d.get("library_id", ""),
        path=d.get("path", ""),
        issues=d.get("issues", []),
        add_file_to_pending_tasks=d.get("add_file_to_pending_tasks", False),
        priority_score=d.get("priority_score", 0),
        shared_info=d.get("shared_info", {}),
    )


@dataclass
class OnWorkerProcessData:
    """
    The 'data' object argument includes:
        worker_log              - Array, the log lines that are being tailed by the frontend. Can be left empty.
        library_id              - Number, the library that the current task is associated with.
        exec_command            - Array, a subprocess command that Unmanic should execute. Can be empty.
        command_progress_parser - Function, a function that Unmanic can use to parse the STDOUT of the command to collect progress stats. Can be empty.
        file_in                 - String, the source file to be processed by the command.
        file_out                - String, the destination that the command should output (may be the same as the file_in if necessary).
        original_file_path      - String, the absolute path to the original file.
        repeat                  - Boolean, should this runner be executed again once completed with the same variables.
    """

    worker_log: List[str]
    library_id: str

    # Can be False to stop command execution
    exec_command: Union[False, List[str]]

    # TODO(Peter): What are the parameter types, what are the return types?
    command_progress_parser: Optional[Callable[[Any], None]]

    file_in: str
    file_out: str
    original_file_path: str
    repeat: bool

    def as_dict(self) -> Dict[str, Any]:
        return {
            "worker_log": self.worker_log,
            "library_id": self.library_id,
            "exec_command": self.exec_command,
            "command_progress_parser": self.command_progress_parser,
            "file_in": self.file_in,
            "file_out": self.file_out,
            "original_file_path": self.original_file_path,
            "repeat": self.repeat,
        }


def on_worker_process_data_make_from_dict(d: Dict[str, Any]) -> OnWorkerProcessData:
    return OnWorkerProcessData(
        worker_log=d.get("worker_log", []),
        library_id=d.get("library_id", ""),
        exec_command=d.get("exec_command", False),
        command_progress_parser=d.get("command_progress_parser", None),
        file_in=d.get("file_in", ""),
        file_out=d.get("file_out", ""),
        original_file_path=d.get("original_file_path", ""),
        repeat=d.get("repeat", False),
    )


@dataclass
class OnPostProcessorFileMovement:
    """
    The 'data' object argument includes:
        source_data             - Dictionary containing data pertaining to the original source file.
        remove_source_file      - Boolean, should Unmanic remove the original source file after all copy operations are complete.
        copy_file               - Boolean, should Unmanic run a copy operation with the returned data variables.
        file_in                 - The converted cache file to be copied by the postprocessor.
        file_out                - The destination file that the file will be copied to.
    """

    source_data: Dict[str, Any]
    remove_source_file: bool
    copy_file: bool
    file_in: str
    file_out: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "source_data": self.source_data,
            "remove_source_file": self.remove_source_file,
            "copy_file": self.copy_file,
            "file_in": self.file_in,
            "file_out": self.file_out,
        }


def on_post_processor_file_movement_make_from_dict(
    d: Dict[str, Any]
) -> OnPostProcessorFileMovement:
    return OnPostProcessorFileMovement(
        source_data=d.get("source_data", {}),
        remove_source_file=d.get("remove_source_file", False),
        copy_file=d.get("copy_file", False),
        file_in=d.get("file_in", ""),
        file_out=d.get("file_out", ""),
    )


@dataclass
class _Settings:
    TEMPORARY_DOWNLOAD_DIRECTORY = ("Temporary Download Directory",)
    OPENSUBTITLES_API_KEY = "OpenSubtitles API Key"


class Settings(PluginSettings):
    settings = {
        # The directory that we will use for downloading temporary files
        # This can include anything "in progress" as well as binary tools like "alass"
        _Settings.TEMPORARY_DOWNLOAD_DIRECTORY: "",
        # The OpenSubtitles API Key
        _Settings.OPENSUBTITLES_API_KEY: "",
    }


def on_library_management_file_test(
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Runner function - enables additional actions during the library management file tests.
    The 'data' object argument includes:
        library_id                      - The library that the current task is associated with
        path                            - String containing the full path to the file being tested.
        issues                          - List of currently found issues for not processing the file.
        add_file_to_pending_tasks       - Boolean, is the file currently marked to be added to the queue for processing.
        priority_score                  - Integer, an additional score that can be added to set the position of the new task in the task queue.
        shared_info                     - Dictionary, information provided by previous plugin runners. This can be appended to for subsequent runners.
    :param data:
    :return:
    """
    dc = on_library_management_file_test_make_from_dict(data)
    print(_LIBRARY_ID, data, dc)
    return dc.as_dict()


def on_worker_process(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runner function - enables additional configured processing jobs during the worker stages of a task.

    The 'data' object argument includes:
        worker_log              - Array, the log lines that are being tailed by the frontend. Can be left empty.
        library_id              - Number, the library that the current task is associated with.
        exec_command            - Array, a subprocess command that Unmanic should execute. Can be empty.
        command_progress_parser - Function, a function that Unmanic can use to parse the STDOUT of the command to collect progress stats. Can be empty.
        file_in                 - String, the source file to be processed by the command.
        file_out                - String, the destination that the command should output (may be the same as the file_in if necessary).
        original_file_path      - String, the absolute path to the original file.
        repeat                  - Boolean, should this runner be executed again once completed with the same variables.

    :param data:
    :return:
    """
    dc = on_worker_process_data_make_from_dict(data)
    print(_LIBRARY_ID, data, dc)
    return dc.as_dict()


def on_postprocessor_file_movement(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runner function - configures additional postprocessor file movements during the postprocessor stage of a task.

    The 'data' object argument includes:
        source_data             - Dictionary containing data pertaining to the original source file.
        remove_source_file      - Boolean, should Unmanic remove the original source file after all copy operations are complete.
        copy_file               - Boolean, should Unmanic run a copy operation with the returned data variables.
        file_in                 - The converted cache file to be copied by the postprocessor.
        file_out                - The destination file that the file will be copied to.

    :param data:
    :return:
    """
    dc = on_post_processor_file_movement_make_from_dict(data)
    print(_LIBRARY_ID, data, dc)
    return dc.as_dict()
