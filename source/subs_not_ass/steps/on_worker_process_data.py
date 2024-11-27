#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List, Union, Optional, Dict, Any, Callable


#  Copyright 2024 pyamsoft
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

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
    exec_command: Union[bool, List[str]]

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

def _map(d: Dict[str, Any]) -> OnWorkerProcessData:
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




def on_worker_process_data_make_from_dict(d: Dict[str, Any]) -> OnWorkerProcessData:
    data = _map(d)
    return data