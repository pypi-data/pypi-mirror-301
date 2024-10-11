"""Custom tucan exeptions"""


class TucanError(RuntimeError):
    """General tucan error
    
    If you are coming from another package, use this by default """
    pass

class TucanParsingError(TucanError):
    """raised if tucan reach a known potential dead end in parsing code
    
    e.g. reaching an fortran end statement withoud corresponding context"""


class TucanCppCleaningError(TucanError):
    """raised if tucan reach a known potential dead end while interpreting CPP directives

    e.g. """
    pass
    pass

class TucanCtrlPtsError(TucanError):
    """raised is tucan reach a dead end when building the control points
    
    e.g. interpreting python code with spurious indentations"""
    pass