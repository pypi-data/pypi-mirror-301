"""Module that aims to analyze a whole package based 
on the other unitary function of the package"""

from typing import Tuple,List
from loguru import logger
from tucan.unformat_main import unformat_main
from tucan.struct_main import struct_main
from tucan.tucanexceptions import TucanError
from tucan.travel_in_package import (
        find_package_files_and_folders,
        scan_wdir
    )
from tucan.struct_common import aggregate_folder_struct

def run_unformat(clean_paths: list) -> dict:
    """
    Gather the unformated version of code files within a dict.

    Args:
        clean_paths (list): List of cleaned paths.

    Returns:
        dict: File path as key, item as a list of lines with their line number span
    """
    statements = {}
    for file in clean_paths:
        statements[file] = unformat_main(file).to_nob()

        nbr_of_stmt = 0
        if statements[file]:
            nbr_of_stmt = len(statements[file])
        logger.info(f"Found {nbr_of_stmt} statements for {file}")

    return statements


def run_struct(all_paths: dict, ignore_errors:bool=True, only_procedures=False, verbose:bool=False) -> dict:
    """
    Gather the data associated to the functions within a file.

    Args:
        clean_paths (list): List of cleaned paths.

    Returns:
        dict: File path as key, item as dict with function names and their data (NLOC, CCN, etc.)
    """
    file_struct = {}
    files = []

    #files = clean_extensions_in_paths(files)
    for file, path in all_paths.items():
        try:
            struct = struct_main(path, verbose=verbose)

            if only_procedures: 
                to_remove=[]
                for part, data in struct.items():
                    if data["type"] in ["file"]:
                        to_remove.append(part)
                for part in to_remove:
                    del struct[part]

            file_struct[file] = struct

        except TucanError:
            logger.warning(f"Struct analysis failed on {file}")
            if ignore_errors:
                file_struct[file] = {}
            else:
                userinput = input("Would you like to continue (y/n)?")
                if userinput == "y":
                    file_struct[file] = {}
                else:
                    raise # raise previous error

    return file_struct

def run_struct_all_repo(
        path: str,
        ignoreerrors:bool=False,
        verbose:bool=False,
        mandatory_patterns: List[str]=None,
        forbidden_patterns: List[str]=None,)->Tuple[dict,dict]:
    logger.info("Recursive path gathering ...")
    paths_dict = find_package_files_and_folders(path,mandatory_patterns=mandatory_patterns,forbidden_patterns=forbidden_patterns)
    logger.info("Running struct ...")
    full_analysis = run_struct(paths_dict,ignore_errors=ignoreerrors, verbose=verbose)
    repo_struct = scan_wdir(path)
    struct_repo = aggregate_folder_struct(repo_struct,full_analysis)
    return struct_repo,full_analysis