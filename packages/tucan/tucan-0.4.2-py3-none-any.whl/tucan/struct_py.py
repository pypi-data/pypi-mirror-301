import re
from typing import Tuple, List
from loguru import logger
from tucan.unformat_common import Statements
from tucan.struct_common import (
    new_buffer_item,
    new_stack_item,
    struct_from_stack,
    struct_augment,
    list2pathref,
)
from tucan.string_utils import find_words_before_left_parenthesis_noregexp

from tucan.kw_lang import KEYWORDS_PY, CONTROL_PTS_PY_ACTIVE, CONTROL_PTS_PY_PASSIVE, CONTROL_LOOPS_PY
from tucan.complexities import (
    halstead_numbers,
    halstead_properties,
    count_ctrl_pts,
    compute_possible_paths,
)
from  tucan.tucanexceptions import TucanCtrlPtsError

def extract_struct_py(statements: Statements, filelabel: str, verbose: bool) -> dict:
    """Main calls to build structure form statements

    statements is the output of tucan.unformat_py.unformat_py
    """
    # TODO: verbose not supported for python
    clean_code = statements.to_code()
    all_structs = _extract_on_cleaned_py(statements, filelabel,verbose)
    all_structs = struct_augment(
        all_structs,
        clean_code,
        find_callables_py,
        compute_complexities_py,
        compute_cst_py,
    )
    for part, data in all_structs.items():
        if data["type"] == "class":
            data["parents"].extend(find_class_inheritance(data["linestart"]))
    return all_structs


def _extract_on_cleaned_py(stmts: Statements, filelabel: str, verbose: bool) -> dict:
    """Extract structure from cleaned statements."""
    path = []
    buffer_pile = []
    stack = []
    
    
    # First file item
    line, (line_idx1, line_idx2) = "", (1, 1)
    stat_idx = 0
    path.append(filelabel)
    buffer_pile.append(
        new_buffer_item(
                    type_="file",
                    path=path,
                    name=filelabel,
                    first_line=line,
                    line_idx=line_idx1,
                    statement_idx=stat_idx,
                    verbose=verbose,
                )
    )
    last_indent = 0
    last_line = None
    
    for stat_idx ,(line, (line_idx1, line_idx2)) in enumerate(zip(stmts.stmt, stmts.lines)):

        indent = int(len(re.findall(r"\s{4}|\s\t+", line)))

        # Find correctly the indentation without accessing spaces in strings
        indent = re.findall(r"^\s+", line)
        if indent:
            indent = int(len(indent[0]) / 4)
        else:
            indent = 0

        # Evaluate indentation level for path and buffer
        if indent > last_indent:
            if indent > last_indent + 1:
                logger.warning(
                    f"Multiple indent at {path} for '({line_idx1}-{line_idx1}){line}' with last indent : {last_indent} and current : {indent}"
                )
                indent = last_indent + 1
            type_, name = parse_name_py(last_line)

            path.append(name)
            buffer_pile.append(
                new_buffer_item(
                    type_=type_,
                    path=path,
                    name=name,
                    first_line=last_line,
                    line_idx=last_idx,
                    statement_idx=stat_idx,
                    verbose=verbose,
                )
            )
            last_line = line
            last_idx = line_idx2
            last_indent = indent
            continue

        elif indent < last_indent:
            for _ in range(last_indent - indent):
                last_buff = buffer_pile[-1]
                stack.append(new_stack_item(last_buff, last_idx, stat_idx, line))
                path.pop(-1)
                buffer_pile.pop(-1)
            last_line = line
            last_indent = indent
            last_idx = line_idx1
            continue

        last_line = line
        last_indent = indent
        last_idx = line_idx1
    
    #close the file item
    stack.append(
        new_stack_item(buffer_pile[-1], line_idx2, stat_idx+1, line, verbose=verbose)
    )
    path.pop(-1)
    buffer_pile.pop(-1)

    struct = struct_from_stack(
        stack, main_types=["file", "def", "class"], skip_types=["if", "for"]
    )

    struct = explicit_methods(struct)

    return struct


def explicit_methods(struct: dict):
    """prepend names of methods by their classes name"""
    for part, data in struct.items():
        path = data["path"]
        if len(path) > 1:
            father_part = list2pathref(path[:-1])
            if father_part in struct:
                if struct[father_part]["type"] == "class":
                    data["name"] = struct[father_part]["name"] + "." + data["name"]
                    data["type"] = "method"
    return struct


def parse_name_py(line: str) -> Tuple[str, str]:
    """expect a lowercase stripped line
    takes the second word as the name
    """
    type_ = line.strip().split()[0]

    try:
        name = line.strip().replace("(", " ").split()[1].replace(":", " ").split()[0]
    except IndexError:
        name = "dummy"

    return type_, name


##### Main structs


def find_callables_py(tokenized_code: List[list]) -> list:
    """Find callables in python"""
    candidates = []
    for tokens in tokenized_code:
        # if not line.strip().startswith("def") and not line.strip().startswith("class"):
        candidates.extend(find_words_before_left_parenthesis_noregexp(tokens))
    matches = [cand.strip() for cand in set(candidates) if cand not in KEYWORDS_PY]

    return sorted(matches)  # Must be sorted for testing


def find_annotations_from_args_py(line: str) -> dict:
    """Find annotation in arguments"""
    id1 = line.find("(")
    id2 = line.rfind(")")
    out = {}
    for arg in line[id1 + 1 : id2].split(","):
        if ":" in arg:
            arg, type_ = arg.split("=")[0].split(":")
            out[arg] = type_
    return out


def find_class_inheritance(line: str) -> list:
    """Find the potential inheritance in a class"""
    id1 = line.find("(")
    id2 = line.rfind(")")
    if id1 == -1:
        return []

    out = line[id1 + 1 : id2].strip()
    if "," in out:
        return [item.strip() for item in out.split(",")]
    elif len(out) == 0:
        return []
    else:
        return [out]



def build_py_ctrl_points(indents: List[int],code: List[list])-> list:
    """build the nested list of control points for python"""
    
    if code == []:
        return []
    
    increment_control_pts = CONTROL_PTS_PY_ACTIVE
    constant_control_pts = CONTROL_PTS_PY_PASSIVE
    
    listpath=[]
    root_path=[]

    # get exhaustive list of levels
    last_lvl=indents[0]
    last_token_line=code[0]
    for current_lvl,tokens_line in zip(indents[1:],code[1:]):
        try: 
            anchor = last_token_line[0]
        except IndexError:
            anchor = None

        if current_lvl>last_lvl:
            root_path.append(anchor)
            listpath.append(root_path.copy())
            
        if current_lvl<last_lvl:
            while current_lvl<last_lvl:
                try:
                    root_path.pop(-1)
                except IndexError:
                    msg_err="Error while building controlpoints. Check the indentation maybe?"
                    logger.warning(msg_err)
                    raise TucanCtrlPtsError(msg_err)
                last_lvl-=1
        
        last_lvl=current_lvl
        last_token_line=tokens_line

    # remove non-control-points levels      
    for i,path in enumerate(listpath):
        listpath[i] =  [item for item in path if item in increment_control_pts+constant_control_pts]

    # move to a nested list
    ctrl_points = [[]]
    for path in listpath:
        if path == []:
            continue
        inserter=ctrl_points
        for _ in path:
            inserter=inserter[-1]
        inserter.extend([path[-1],[]])
    ctrl_points=ctrl_points[0]
    return ctrl_points


def compute_complexities_py(indents_code: List[int], tokenized_code: List[list]) -> int:
    """Count decision points (if, else if, do, select, etc.)"""
    indents_code=[ind/4 for ind in indents_code]
    avg_indent = sum(indents_code[1:])/len(indents_code[1:])
    #ctrls_pts = build_py_ctrl_points(indents_code[1:],tokenized_code[1:])
    mccabe = count_ctrl_pts(tokenized_code[1:],CONTROL_PTS_PY_ACTIVE+CONTROL_PTS_PY_PASSIVE)
    loops = count_ctrl_pts(tokenized_code[1:],CONTROL_LOOPS_PY)
    #possible_paths = compute_possible_paths(ctrls_pts,active_ctl_pts=CONTROL_PTS_PY_ACTIVE, passive_ctl_pts=CONTROL_PTS_PY_PASSIVE)
    volume, difficulty, effort =  halstead_properties(*halstead_numbers(tokenized_code[1:], KEYWORDS_PY))
    time_to_code = int(effort/18)

    return round(avg_indent,2),mccabe,loops,volume, difficulty,time_to_code


def compute_cst_py(type_: str) -> int:
    """State the structural complexity of a code

    in Short, the average nb. of time we re-read the element.
    It does NOT means it's bad practice
    It just means more read time for the reader to understand the code"""

    cst_ = {"file":0, "def": 1, "class": 4, "method": 2}
    if type_ not in cst_:
        logger.warning(f"Type {type_} not present in conversion list ")
        return 1

    return cst_.get(type_, 1)
