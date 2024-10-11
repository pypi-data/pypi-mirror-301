"""Global function to handle the struct analysis of various languages"""
from os.path import splitext, basename
from loguru import logger
from tucan.supported_files import SOURCES_C,SOURCES_FTN,SOURCES_PY,HEADERS_C_FTN
from tucan.unformat_common import read_lines_with_encoding
from tucan.unformat_py import unformat_py
from tucan.unformat_ftn import unformat_ftn
from tucan.unformat_c import unformat_c
from tucan.struct_py import extract_struct_py
from tucan.struct_ftn import extract_struct_ftn
from tucan.struct_c import extract_struct_c
from tucan.clean_ifdef import remove_ifdef_from_module
from tucan.guess_language import guess_language


def struct_main(filename: str, verbose: bool = False) -> dict:
    """
    Extract structure of a fortran or python file.
    - Find the nested structures of a code
    - Find the callables in each structure
    - Evaluate sizes, CCN

    Args:
        filename (str): Name of the file (with its path) to parse.

    Returns:
        dict: Structure analyzed, with complexity, size, name, path, lines span, etc.

        void dictionary if failed.

    """

    logger.info(f"Struct analysis on {filename}")
    code = read_lines_with_encoding(filename)

    code = [line.lower() for line in code]  # Lower case for all

    filelabel = splitext(basename(filename))[0]

    if filename.lower().endswith(SOURCES_PY):
        logger.debug(f"Python code detected ...")
        statements = unformat_py(code)
        struct_ = extract_struct_py(statements, filelabel, verbose)
    elif filename.lower().endswith(SOURCES_FTN):
        logger.debug(f"Fortran code detected ...")
        code = remove_ifdef_from_module(code, [], verbose=False, fortran=True)
        statements = unformat_ftn(code)
        struct_ = extract_struct_ftn(statements, filelabel, verbose)
    elif filename.lower().endswith(SOURCES_C):
        logger.debug(f"C/C++ code detected ...")
        code = remove_ifdef_from_module(code, [], verbose=False)
        statements = unformat_c(code)
        struct_ = extract_struct_c(statements, filelabel, verbose)
    elif filename.lower().endswith(HEADERS_C_FTN):
        lang = guess_language(code)
        logger.info(f"Language of .h file is ({lang}), ")

        if lang in ["fortran"]:
            logger.debug(f"Fortran code detected ...")
            code = remove_ifdef_from_module(code, [], verbose=False, fortran=True)
            statements = unformat_ftn(code)
            struct_ = extract_struct_ftn(statements, filelabel, verbose)
        else:  # lang in ["ccpp"]:
            logger.debug(f"C/C++ code detected ...")
            code = remove_ifdef_from_module(code, [], verbose=False)
            statements = unformat_c(code)
            struct_ = extract_struct_c(statements, filelabel, verbose)

    else:
        ext = filename.lower().split(".")[-1]
        logger.error(f"Extension {ext} not supported, exiting ...")
        return {}

    return struct_

