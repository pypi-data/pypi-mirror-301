__author__ = "aiXplain"

"""
Copyright 2023 The aiXplain SDK authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: aiXplain team
Date: March 20th 2023
Description:
    File Type Enum
"""

from enum import Enum


class FileType(Enum):
    CSV = ".csv"
    JSON = ".json"
    TXT = ".txt"
    XML = ".xml"
    FLAC = ".flac"
    MP3 = ".mp3"
    WAV = ".wav"
    JPEG = ".jpeg"
    PNG = ".png"
    JPG = ".jpg"
    GIF = ".gif"
    WEBP = ".webp"
    AVI = ".avi"
    MP4 = ".mp4"
    MOV = ".mov"
    MPEG4 = ".mpeg4"
