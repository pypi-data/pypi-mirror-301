#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ==============================================================================
# Copyright (c) 2024 laugh12321 Authors. All Rights Reserved.
#
# Licensed under the GNU General Public License v3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# File    :   c_lib_wrap.py
# Version :   1.0
# Author  :   laugh12321
# Contact :   laugh12321@vip.qq.com
# Date    :   2024/07/03 13:12:29
# Desc    :   A script to locate and load necessary CUDA and TensorRT libraries.
# ==============================================================================
import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional

from loguru import logger

logger.configure(handlers=[{'sink': sys.stdout, 'colorize': True, 'format': "<level>[{level.name[0]}]</level> <level>{message}</level>"}])


def find_library(base_path: Path, lib_name: str) -> Optional[Path]:
    """
    Find the path of a specific library.

    Args:
        base_path (Path): The base path to search.
        lib_name (str): The name of the library.

    Returns:
        Optional[Path]: The path of the found library, or None if not found.
    """
    patterns = {
        "cudart": re.compile(r'cudart64_\d+\.dll'),
        "cudnn": re.compile(r'cudnn64_\d+\.dll'),
        "nvinfer": re.compile(r'nvinfer(_\d+)?\.dll'),
    }
    file_patterns = {
        "cudart": 'cudart64_*.dll',
        "cudnn": 'cudnn64_*.dll',
        "nvinfer": 'nvinfer*.dll',
    }
    pattern = patterns.get(lib_name)
    file_pattern = file_patterns.get(lib_name)

    if not pattern or not file_pattern:
        return None

    for path in base_path.rglob(file_pattern):
        if pattern.match(path.name):
            return path.parent

    return None


def check_libs(libs_dir: Dict[str, Path]) -> bool:
    """
    Check if all necessary libraries are found.

    Args:
        libs_dir (Dict[str, Path]): A dictionary containing library paths.

    Returns:
        bool: True if all libraries are found, False otherwise.
    """
    required_libs = {"cudart", "cudnn", "nvinfer"}
    if required_libs.issubset(libs_dir):
        import json

        logger.info(
            f"Successfully found necessary library paths:\n{json.dumps({key: str(value) for key, value in libs_dir.items()}, indent=4)}"
        )
        return True
    return False


def update_libs(user_specified_dir: Path, libs_dir: Dict[str, Path]) -> bool:
    """
    Update library directories and check if all libraries are found.

    Args:
        user_specified_dir (Path): The directory to check.
        libs_dir (Dict[str, Path]): A dictionary to store library paths.

    Returns:
        bool: True if all libraries are found, False otherwise.
    """
    for lib_name in ["cudart", "cudnn", "nvinfer"]:
        if libs_dir.get(lib_name) is None:
            path = find_library(user_specified_dir, lib_name)
            if path is not None:
                libs_dir[lib_name] = path

    return check_libs(libs_dir)


def add_dll_search_dir(dir_path: Path) -> None:
    """
    Add a DLL search path.

    Args:
        dir_path (Path): The directory path to add.
    """
    os.environ["PATH"] = str(dir_path) + ";" + os.environ["PATH"]
    sys.path.insert(0, str(dir_path))
    if sys.version_info[:2] >= (3, 8):
        os.add_dll_directory(str(dir_path))


if os.name == "nt":
    libs_dir: Dict[str, Path] = {}
    need_lib_dirs = [Path(r"/usr/local/cuda-12.5"), Path(r"/usr/local/tensorrt")]
    sys_paths = [Path(p) for p in os.environ["PATH"].strip().split(";")]

    for need_lib_dir in need_lib_dirs:
        if update_libs(need_lib_dir, libs_dir):
            break

    if not check_libs(libs_dir):
        for sys_path in sys_paths:
            if update_libs(sys_path, libs_dir):
                break

    current_path = Path(__file__).resolve()
    dirname = current_path.parent
    build_libs_dir = dirname / "libs"
    all_dirs = list(set(libs_dir.values()) | {build_libs_dir})

    for dir in all_dirs:
        if dir.exists():
            add_dll_search_dir(dir)

try:
    from .libs.pydeploy import *
except Exception as e:
    raise RuntimeError(f"Deploy initialization failed! Error: {e}")
