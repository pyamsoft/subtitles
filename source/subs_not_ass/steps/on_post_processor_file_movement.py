#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Dict, Any

from source.subs_not_ass.settings import Settings


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
class OnPostProcessorFileMovement:
    """
    The 'data' object argument includes:
        library_id              - Number, the library that the current task is associated with.
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

def _map(
        d: Dict[str, Any]
) -> OnPostProcessorFileMovement:
    return OnPostProcessorFileMovement(
        source_data=d.get("source_data", {}),
        remove_source_file=d.get("remove_source_file", False),
        copy_file=d.get("copy_file", False),
        file_in=d.get("file_in", ""),
        file_out=d.get("file_out", ""),
    )


def on_post_processor_file_movement_make_from_dict(
        d: Dict[str, Any]
) -> OnPostProcessorFileMovement:
    data = _map(d)
    return data
