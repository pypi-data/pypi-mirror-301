"""
Tucan module to handle the import parsing of all files.
"""
from typing import List
import json
from loguru import logger
from tucan.supported_files import (
    SOURCES_C,
    SOURCES_FTN,
    SOURCES_PY,
    HEADERS_C_FTN,
    ALL_SUPPORTED_EXTENSIONS,
)
from tucan.unformat_common import read_lines_with_encoding
from tucan.guess_language import guess_language
from tucan.imports_py import get_imports_py
from tucan.imports_ftn import get_imports_ftn
from tucan.imports_c import get_imports_ccpp
from tucan.unformat_py import unformat_py

from tucan.travel_in_package import find_package_files_and_folders
from tucan.string_utils import (
    get_common_root_index_list,
    tokenize,
    best_front_match,
    best_inner_match,
)
from tucan.string_utils import generate_dict_paths


def imports_of_file(filename: str, verbose: bool = False) -> dict:
    """
    Extract the imports of a code file.

    Args:
        filename (str): Name of the file (with its path) to parse.

    Returns:
        dict: Imports functions stored by filename as key.
    """
    logger.info(f"Analyzing the imports for {filename}")

    code = read_lines_with_encoding(filename)
    # not Lower cased !

    if filename.lower().endswith(SOURCES_PY):
        logger.debug(f"Python code detected ...")
        imps = get_imports_py(unformat_py(code).to_code())
    elif filename.lower().endswith(SOURCES_FTN):
        logger.debug(f"Fortran code detected ...")
        imps = get_imports_ftn(code)
    elif filename.lower().endswith(SOURCES_C):
        logger.debug(f"C/C++ code detected ...")
        imps = get_imports_ccpp(code)
    elif filename.lower().endswith(HEADERS_C_FTN):
        lang = guess_language(code)
        if lang in ["ccpp"]:
            logger.debug(f"C/C++ code detected ...")
            imps = get_imports_ccpp(code)
        elif lang in ["fortran"]:
            logger.debug(f"Fortran code detected ...")
            imps = get_imports_ftn(code)
        else:
            logger.debug(f"Language was not either C or Fortran, skipping...")
            imps = {}
    else:
        ext = filename.lower().split(".")[-1]
        logger.error(f"Extension {ext} not supported, exiting ...")
        imps = {}

    return imps, len(code)


def imports_of_repository(
    path: str,
    mandatory_patterns: List[str] = None,
    forbidden_patterns: List[str] = None,
) -> dict:
    paths_dict = find_package_files_and_folders(
        path,
        mandatory_patterns=mandatory_patterns,
        forbidden_patterns=forbidden_patterns,
    )

    paths = [path_.split("/") for path_ in paths_dict.values()]

    idx = get_common_root_index_list(paths)
    root = paths[0][:idx]
    # print(json.dumps(paths, indent=4))

    paths = [path_[idx:] for path_ in paths]

    def _full_path(root: list, path_: list) -> str:
        return "/".join(root) + "/" + "/".join(path_)

    tree_dict = {}
    for path_ in paths:
        current = tree_dict
        for bit in path_:
            if bit not in current:
                current[bit] = {}
            if bit.endswith(SOURCES_FTN):
                fname = _full_path(root, path_)
                current[bit] = {key: {} for key in search_for_modules(fname)}
            current = current[bit]

    # tree_nob = Nob(tree_dict)
    tree_paths = generate_dict_paths(tree_dict)
    imports = {}
    sizes = {}
    for path_ in paths:
        local_imports = []
        imps_of_file, size_of_file = imports_of_file(_full_path(root, path_))
        for imps in imps_of_file.values():
            # logger.critical(path_)
            ref = find_import_ref(tree_paths, imps, orig_file="/".join(path_))
            if ref is not None:
                local_imports.append(ref)

        imports["/".join(path_)] = sorted(set(local_imports))
        sizes["/".join(path_)] = size_of_file

    return imports, sizes


def search_for_modules(filename: str) -> set:
    out = []
    code = [line.lower() for line in read_lines_with_encoding(filename)]
    for line in code:
        if line.lstrip().startswith("module"):
            out.append(tokenize(line)[1])
    return out


def remove_py_in_keys(dict_: dict) -> dict:
    """return the same dictionary but removong the .py in keys"""

    def _rec_no_py(indict_: dict) -> dict:
        """recursive, returning same dico w.o. .py in keys"""
        out = {}
        for key in indict_:
            out[key.replace(".py", "")] = _rec_no_py(indict_[key])
        return out

    return _rec_no_py(dict_)


def _find_import_by_file(tree_paths: list, file_ref: str) -> List[str]:
    hint = file_ref.split("/")

    # logger.warning(f"finding {hint} in {tree_paths}")
    imatch = best_inner_match(hint, tree_paths)
    # logger.warning(f"out is {imatch}")
    if imatch == []:
        return [f"__external__/{file_ref}"]

    out = ["/".join(stop_to_file(tree_paths[i])) for i in imatch]
    return out


def _find_import_for_ftn(tree_paths: list, mod_ref: str) -> List[str]:
    hint = mod_ref.split(".")
    # logger.info(f"In{hint}")
    # logger.info(f"TP{tree_paths}")
    # list_splited_paths = [_path.split("/") for _path in tree_paths]
    imatch = best_inner_match(hint, tree_paths)
    # logger.info(f"IM{imatch}")

    if imatch == []:
        return [f"__external__/{mod_ref}"]

    out = ["/".join(stop_to_file(tree_paths[i])) for i in imatch]
    return out


def _find_import_for_python(tree_paths: list, mod_ref: str) -> List[str]:
    hint = mod_ref.split(".")
    # logger.info(f"In{hint}")
    # logger.info(f"TP{tree_paths}")
    list_paths = ["/".join(path_) for path_ in tree_paths]
    # logger.info(f"LP{list_paths}")
    list_nopy_paths = [_path.replace(".py", "").split("/") for _path in list_paths]
    # logger.info(f"NP{list_nopy_paths}")

    imatch = best_inner_match(hint, list_nopy_paths)
    # logger.info(f"im{imatch}")

    if imatch == []:
        return [f"__external__/{mod_ref}"]

    out = ["/".join(stop_to_file(list_paths[i].split("/"))) for i in imatch]
    # logger.info(f"im{out}")
    return out


def find_import_ref(tree_paths: list, hint: str, orig_file: str = None) -> str:
    """Resolve import puzzles"""

    hint = hint.rstrip("*").rstrip(".")
    file_ref, mod_ref = hint.split("@")

    if file_ref == "__py__":
        matches = _find_import_for_python(tree_paths, mod_ref)
    elif file_ref == "__ftn__":
        matches = _find_import_for_ftn(tree_paths, mod_ref)
    else:
        matches = _find_import_by_file(tree_paths, file_ref)

    # logger.info(f"==> {hint} out {matches} in file {orig_file}")
    out = matches[0]
    if len(matches) > 1:
        if orig_file is None:
            out = matches[0]
        else:
            out = best_front_match(orig_file, matches)

    return out


def stop_to_file(path_l: List[str]) -> List[str]:
    out = []
    for item in path_l:
        out.append(item)
        if "." + item.split(".")[-1] in ALL_SUPPORTED_EXTENSIONS:
            break
    return out
