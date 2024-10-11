from pathlib import Path
from typing import List
import os
import fnmatch
from glob import glob

# from ctypes import c_int64  # amutable int
from loguru import logger

from tucan.supported_files import ALL_SUPPORTED_EXTENSIONS


def find_package_files_and_folders(
    path: str,
    mandatory_patterns: List[str] = None,
    forbidden_patterns: List[str] = None,
) -> dict:
    paths = _rec_travel_through_package(
        path,
        mandatory_patterns=mandatory_patterns,
        forbidden_patterns=forbidden_patterns,
    )
    return _get_package_files(paths, path)


def _rec_travel_through_package(
    path: str,
    mandatory_patterns: List[str] = None,
    forbidden_patterns: List[str] = None,
) -> list:
    """
    List all paths from a folder and its sub-folders recursively.

    RECURSIVE
    """

    def _is_valid_path(path, mandatory_patterns, forbidden_patterns):
        if mandatory_patterns is not None:
            match = False
            for ptn in mandatory_patterns:
                if fnmatch.filter([path], ptn):
                    match = True
            if not match:  # path match no mandatory patterns
                logger.warning(
                    f"filter {path} does not match any mandatory patterns {mandatory_patterns}"
                )
                return False

        if forbidden_patterns is None:
            return True

        for ptn in forbidden_patterns:
            if fnmatch.filter([path], ptn):
                logger.warning(f"filter {path} match forbidden pattern {ptn}")
                return False  # path match one forbidden pattern
        logger.success(f"filter {path} is OK")
        return True

    paths_ = []
    current_path = Path(path)
    for element in current_path.iterdir():
        path_str = element.as_posix()
        if _is_valid_path(path_str, mandatory_patterns, forbidden_patterns):
            if element.is_dir():
                paths_.extend(
                    _rec_travel_through_package(
                        path_str,
                        mandatory_patterns=mandatory_patterns,
                        forbidden_patterns=forbidden_patterns,
                    )
                )
            else:
                if not path_str.endswith(ALL_SUPPORTED_EXTENSIONS):
                    continue
                if path_str not in paths_:
                    if not path_str.split("/")[-1].startswith("."):
                        paths_.append(path_str)

    return paths_


def _get_package_files(clean_paths: list, relpath: str) -> dict:
    """
    Return all the files useful for a package analysis, with their absolut paths

    """

    files = []
    for path_ in clean_paths:
        if not Path(path_).is_dir():
            #            logger.info(f"Append :{path_}")
            files.append(path_)

    files = _clean_extensions_in_paths(files)

    if not files:
        logger.warning(f"No files found in the paths provided")

    files = [Path(p_) for p_ in files]

    out = {}
    for file in files:
        path_ = file.relative_to(Path(relpath)).as_posix()
        out[path_] = file.as_posix()

    return out


def _clean_extensions_in_paths(paths_list: list) -> list:
    """
    [PRIVATE] Remove unwanted path extensions and duplicates.

    Args:
        paths_list (list): List of all paths gatheres through recursive analysis

    Returns:
        list: List of cleaned paths.
    """
    clean_paths = []
    for path in paths_list:
        if path.endswith(ALL_SUPPORTED_EXTENSIONS):
            clean_paths.append(path)

    return [
        *set(clean_paths),
    ]


def scan_wdir(wdir):
    """Build the structure of a folder tree.

    :params wdir: path to a directory
    """

    def _rec_subitems(path: str):  # , item_id):
        file = Path(path)

        type_ = "folder"
        if file.is_file():
            type_ = "file"
            if file.suffix not in ALL_SUPPORTED_EXTENSIONS:
                return None
        out = {
            "name": file.name,
            "relpath": file.relative_to(Path(wdir)).as_posix(),
            "type": type_,
        }

        if file.is_dir():
            out["children"] = list()
            for nexpath in glob(os.path.join(path, "**")):
                record = _rec_subitems(nexpath)
                if record is not None:
                    out["children"].append(record)
        return out

    out = _rec_subitems(wdir)  # , 0, item_id=c_int64(-1))]

    return out
