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

from dataclasses import dataclass

from unmanic.libs.unplugins.settings import PluginSettings

@dataclass
class SettingsKeys:
    TOOLS_DIRECTORY = "Tools Directory"
    OPENSUBTITLES_API_KEY = "OpenSubtitles API Key"
    OVERWRITE_ORIGINAL_SRT = "Overwrite Original Subtitles With Fixed Copy"

class Settings(PluginSettings):

    settings = {
        # The directory that we will use for downloading temporary files
        # This can include anything "in progress" as well as binary tools like "alass"
        SettingsKeys.TOOLS_DIRECTORY: "",
        # The OpenSubtitles API Key
        SettingsKeys.OPENSUBTITLES_API_KEY: "",
        # Overwrite the original subtitles with the fixed copy
        SettingsKeys.OVERWRITE_ORIGINAL_SRT: False,
    }

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
