"""Global function to handle the unformat of various languages"""
from loguru import logger

from tucan.supported_files import SOURCES_C,SOURCES_FTN,SOURCES_PY,HEADERS_C_FTN
from tucan.guess_language import guess_language
from tucan.unformat_common import read_lines_with_encoding
from tucan.unformat_py import unformat_py
from tucan.unformat_ftn import unformat_ftn
from tucan.unformat_c import unformat_c
from tucan.clean_ifdef import remove_ifdef_from_module


def unformat_main(filename: str, verbose: bool = False) -> list:
    """
    Main function to call to get an unformated version of the code

    Args:
        filename (str): _description_

    Returns:
        list: _description_
    """
    logger.info(f"Unformatting {filename}")

    code = read_lines_with_encoding(filename)

    code = [line.lower() for line in code]  # Lower case for all

    if filename.lower().endswith(SOURCES_PY):
        logger.debug(f"Python code detected ...")
        statements = unformat_py(code)
    elif filename.lower().endswith(SOURCES_FTN):
        logger.debug(f"Fortran code detected ...")
        code = remove_ifdef_from_module(code, [], verbose, fortran=True)
        statements = unformat_ftn(code)
    elif filename.lower().endswith(SOURCES_C):
        logger.debug(f"C/C++ code detected ...")
        code = remove_ifdef_from_module(code, [], verbose)
        statements = unformat_c(code)
    elif filename.lower().endswith(HEADERS_C_FTN):
        lang = guess_language(code)
        if lang in ["ccpp"]:
            logger.debug(f"C/C++ code detected ...")
            code = remove_ifdef_from_module(code, [], verbose=False)
            statements = unformat_c(code)
        elif lang in ["fortran"]:
            logger.debug(f"Fortran code detected ...")
            code = remove_ifdef_from_module(code, [], verbose=False, fortran=True)
            statements = unformat_ftn(code)
        else:
            logger.debug(f"Language was not either C or Fortran, skipping...")
            statements = None
    else:
        ext = filename.lower().split(".")[-1]
        logger.error(f"Extension {ext} not supported, exiting ...")
        statements = None

    return statements
