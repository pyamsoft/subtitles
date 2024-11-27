#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List, Dict, Any


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

def _map(
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


def on_library_management_file_test_make_from_dict(
        d: Dict[str, Any]
) -> OnLibraryManagementFileTestData:
    data = _map(d)
    return data
