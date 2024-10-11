

SOURCES_FTN =(".f", ".F", ".f77", ".F77", ".f90", ".F90")
SOURCES_C = (".c", ".cpp", ".cc")
SOURCES_PY = (".py",) # required with a , ; else the addition will lead to ., p, y,
HEADERS_C_FTN = (".h", ".hpp")

ALL_SUPPORTED_EXTENSIONS = tuple(
    list(SOURCES_FTN)+
    list(SOURCES_C)+
    list(SOURCES_PY)+
    list(HEADERS_C_FTN))
