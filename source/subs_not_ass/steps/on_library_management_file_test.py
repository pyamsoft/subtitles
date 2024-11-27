#!/usr/bin/env python3
import os
import traceback
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union

from watchdog.observers.fsevents2 import message

from source.subs_not_ass.constants import LIBRARY_ID
from source.subs_not_ass.settings import Settings, SettingsKeys

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

_HOOK_NAME = "on_library_management_file_test"


class OnLibraryManagementFileTestException(Exception):

    def __init__(self, message_or_cause: Union[OSError , str]):
        super().__init__(message_or_cause if type(message_or_cause) == "str" else message_or_cause.strerror)
        self.message = message

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

    library_id: int
    path: str
    issues: List[Issue]
    add_file_to_pending_tasks: bool
    priority_score: int
    shared_info: Dict[str, Any]

    def as_dict(self) -> Dict[str, Any]:
        issues: List[Dict[str, Any]] = []
        for issue in self.issues:
            issues.append({
                "id": issue.id,
                "message": issue.message,
            })

        return {
            "library_id": self.library_id,
            "path": self.path,
            "issues": issues,
            "add_file_to_pending_tasks": self.add_file_to_pending_tasks,
            "priority_score": self.priority_score,
            "shared_info": self.shared_info,
        }

def _map(
        d: Dict[str, Any]
) -> OnLibraryManagementFileTestData:
    raw_issues: List[Dict[str, Any]] = d.get("issues", [])

    issues: List[Issue] = []
    for issue in raw_issues:
        issues.append(Issue(
            id=issue.get("id", ""),
            message=issue.get("message", ""),
        ))

    return OnLibraryManagementFileTestData(
        library_id=d.get("library_id", 0),
        path=d.get("path", ""),
        issues=issues,
        add_file_to_pending_tasks=d.get("add_file_to_pending_tasks", False),
        priority_score=d.get("priority_score", 0),
        shared_info=d.get("shared_info", {}),
    )


def _verify_valid_file(data: OnLibraryManagementFileTestData) -> bool:
    abspath = data.path

    # TODO(Peter): Use the FFMPEG Prober submodule instead of comparing off raw file paths?

    if not os.path.exists(abspath):
        data.add_file_to_pending_tasks = False
        return False

    is_valid_ext = abspath.endswith(".mkv") or abspath.endswith(".mp4")
    if not is_valid_ext:
        data.add_file_to_pending_tasks = False
        return False

    return True

def _determine_needs_work(data: OnLibraryManagementFileTestData):
    """A given file will 'need work' if it either has no SRT file, or has no FIXED SRT file"""
    abspath = data.path

    # From the absolute path, get the directory name and file name
    dir_path = os.path.dirname(abspath)
    file_path, file_ext = os.path.splitext(abspath)
    base_file_name = os.path.basename(file_path)

    # We expect an SRT file named the exact same as the media file, but with .srt
    expect_srt_file = f"{dir_path}/{base_file_name}.srt"

    # If we have processed with ALASS, we expect a .FIXED.srt output
    expect_fixed_srt_file = f"{dir_path}/{base_file_name}.FIXED.srt"

    # No SRT, needs work
    if not os.path.exists(expect_srt_file):
        data.add_file_to_pending_tasks = True

    # No fixed SRT, needs work
    if not os.path.exists(expect_fixed_srt_file):
        data.add_file_to_pending_tasks = True

def _verify_tools_directory(settings: Settings) -> str:
    tools_directory: Optional[str] = settings.get_setting(SettingsKeys.TOOLS_DIRECTORY)
    if not tools_directory:
        raise OnLibraryManagementFileTestException("TOOLS_DIRECTORY is required")

    # Ensure the tools directory is created
    try:
        os.makedirs(tools_directory, mode = 0x755, exist_ok= True)
    except OSError as e:
        raise OnLibraryManagementFileTestException(e)

    return tools_directory

def _verify_alass(tools_directory: str):
    alass_path = f"{tools_directory}/alass"
    if not os.path.exists(alass_path):
        raise OnLibraryManagementFileTestException(f"ALASS program expected at {alass_path}")

def _test_work_required(data: OnLibraryManagementFileTestData, settings: Settings):
    if not _verify_valid_file(data):
        return

    tools_directory = _verify_tools_directory(settings)
    _verify_alass(tools_directory)

def on_library_management_file_test_make_from_dict(
        d: Dict[str, Any],
) -> OnLibraryManagementFileTestData:
    data = _map(d)

    try:
        # By default, assume we are not going to operate on this file unless we PASS
        data.add_file_to_pending_tasks = False

        settings = Settings(library_id=data.library_id)

        # Verify that we do need work done
        _test_work_required(data, settings)

        # Determine if we are doing work
        _determine_needs_work(data)
    except OnLibraryManagementFileTestException as e:
        data.issues.append(
            Issue(
                id=LIBRARY_ID,
                message=f"[{_HOOK_NAME}] Error: {e.message}"
            )
        )
    except Exception as e:
        data.issues.append(
            Issue(
                id=LIBRARY_ID,
                message=f"[{_HOOK_NAME}] Unexpected Error: {traceback.format_exception(e)}"
            )
        )
    return data
