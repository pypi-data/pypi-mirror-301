"""
Module that gather the most common functions of struct.
"""

from dataclasses import dataclass
from typing import Tuple, List, Callable
from copy import deepcopy
from loguru import logger
from typing import List
from tucan.complexities import maintainability_index
from tucan.string_utils import tokenize, get_indent



FIELDS_EXT_DICT = {
    "HTM": "Halstead time        ",
    "CST": "Structural complexity",
#    "CPP": "Nb. of Paths         ",
    "LPS": "Nb. of Loops         ",
}

FIELDS_INT_DICT = {
    "CCN": "Ctls. Pts. (McCabe)  ",
    "HDF": "Halstead Difficulty  ",
    "MI":  "Maintainability Index",
    "IDT": "Average indents      ",
}

FIELDS_SIZES_DICT = {
    "ssize": "Nb. Statements",
    "NLOC": "Nb. lines of code",
}

FIELDS_EXTENSIVE = list(FIELDS_EXT_DICT.keys())
FIELDS_SIZES = list(FIELDS_SIZES_DICT.keys())
FIELDS_INTENSIVE = list(FIELDS_INT_DICT.keys())
EPSILON=1e-12
    

def path_clean(path: list, paths_to_clean: Tuple[list]) -> list:
    """Remove the unwanted steps of the paths"""
    indexes_to_clean = []
    for ptc in paths_to_clean:
        if list2pathref(path).startswith(list2pathref(ptc)):
            indexes_to_clean.append(len(ptc) - 1)
    new_path = []
    for i, step in enumerate(path):
        if i not in indexes_to_clean:
            new_path.append(step)
    return new_path


def list2pathref(path: list) -> str:
    """The way we will refer to path here in strings"""
    return ".".join(path)


def pathref_ascendants(pathstr: str) -> List[str]:
    """Return all ascendends of a path"""
    out = []
    path = pathstr.split(".")
    while len(path) > 1:
        path.pop(-1)
        out.append(list2pathref(path))
    return out



########################################################
# BUFFER of detection
@dataclass
class BufferItem:
    """Forces buffers to keep the same logic across languages"""

    type_: str = None
    name: str = None
    path: list = None
    first_line: str = None
    line_idx: int = None
    statement_idx: int = None
    parents: List[str] = None
    callables: List[str] = None
    contains: List[str] = None
    comment: str = None


def new_buffer_item(
    type_: str = None,
    name: str = None,
    path: List[str] = None,
    first_line: str = None,
    line_idx: int = None,
    statement_idx: int = None,
    verbose: bool = False,
    parents: List[str] = None,
    callables: List[str] = None,
    contains: List[str] = None,
    comment: str = None,
) -> BufferItem:
    if verbose:
        fname = ".".join(path)
        logger.critical(f"START l.{line_idx} for " + fname +"|"+type_)
    if parents is None:
        parents = []
    if callables is None:
        callables = []
    if contains is None:
        contains = []
    if comment is None:
        comment = ""
    out = BufferItem(
        type_=type_,
        name=name,
        path=path,
        first_line=first_line,
        line_idx=line_idx,
        statement_idx=statement_idx,
        parents=parents,
        callables=callables,
        contains=contains,
        comment=comment,
    )
    return out


########################################################
# STACK of detection
@dataclass
class StackItem:
    """Forces buffers to keep the same logic across languages"""

    type_: str
    name: str
    path: list
    start_line_idx: int
    start_statement_idx: int
    start_line: str
    end_line_idx: int
    end_statement_idx: int
    end_line: str
    parents: List[str] = None
    callables: List[str] = None
    contains: List[str] = None
    comment: str = None


def new_stack_item(
    buf: BufferItem,
    end_line_idx: int,
    end_statement_idx: int,
    end_line: str,
    verbose: bool = False,
) -> StackItem:
    if verbose:
        fname = ".".join(buf.path)
        logger.critical(f" END   l.{end_line_idx} for " + fname + '|'+end_line.strip())
    out = StackItem(
        type_=buf.type_,
        name=buf.name,
        path=buf.path.copy(),
        start_line_idx=buf.line_idx,
        start_statement_idx=buf.statement_idx,
        start_line=buf.first_line,
        parents=buf.parents,
        callables=buf.callables,
        contains=buf.contains,
        comment=buf.comment,
        end_line_idx=end_line_idx,
        end_statement_idx=end_statement_idx,
        end_line=end_line,
    )
    return out


def struct_from_stack(stack: list, main_types: list, skip_types: list = None) -> dict:
    """Build a dictionary of all structures"""
    # Build nested structure
    struct = {}
    if skip_types is None:
        skip_types = []

    path_to_skip = []
    for stack_item in stack:
        if stack_item.type_ in skip_types:
            path_to_skip.append(stack_item.path)

    for stack_item in stack:
        cleaned_path = path_clean(stack_item.path, path_to_skip)
        if stack_item.type_ in main_types:
            # logger.warning(f"Adding {list2pathref(cleaned_path)}")
            id_ = list2pathref(cleaned_path)
            if id_ not in struct:
                struct[id_] = {
                    "path": cleaned_path,
                    "name": stack_item.name,
                    "type": stack_item.type_,
                    "linestart": stack_item.start_line,
                    "lines": [stack_item.start_line_idx, stack_item.end_line_idx],
                    "statements": [
                        stack_item.start_statement_idx,
                        stack_item.end_statement_idx,
                    ],  # Warning: here statements starts at 1!!!
                    "contains": stack_item.contains,
                    "parents": stack_item.parents,
                    "callables": stack_item.callables,
                    "comment": stack_item.comment,
                    "annotations": {},
                }
            else: # create a proxy because this structure is redefined
                id_new = id_ + f"#{stack_item.start_line_idx},{stack_item.end_line_idx}"
                struct[id_new] = {
                    "path": cleaned_path,
                    "name": stack_item.name,
                    "type": stack_item.type_,
                    "linestart": stack_item.start_line,
                    "lines": [stack_item.start_line_idx, stack_item.end_line_idx],
                    "statements": [
                        stack_item.start_statement_idx,
                        stack_item.end_statement_idx,
                    ],  # Warning: here statements starts at 1!!!
                    "contains": stack_item.contains,
                    "parents": stack_item.parents,
                    "callables": stack_item.callables,
                    "comment": stack_item.comment,
                    "annotations": {},
                }
                struct[id_]["contains"].append(id_new)
            
           

    return struct


# def get_struct_sizes(struct: dict) -> dict:
#     """Compute the size of strict items (statefull)"""
#     struct_aspects = {}
#     for part, data in struct.items():
#         struct_aspects[part] = {}
#         struct_aspects[part]["NLOC"] = data["lines"][-1] - data["lines"][0] + 1
#         struct_aspects[part]["ssize"] = data["statements"][-1] - data["statements"][0]
        
#     return struct_aspects


def replace_self(list_: list, parent: str) -> list:
    """Replace the self keyword in a parentality path"""
    return [item.replace("self.", parent + ".") for item in list_]


def _strip_safe_lines(beg: int, end: int, safes: List[list]) -> List:
    """Return an iterable stripped from safe zones
    beg=100
    end = 110
    safes = [[103,104],[106,109]]

    100
    101
    102
    105

    """
    iter_ = []
    for i in range(beg, end + 1):
        blocked = False
        for safe in safes:
            if i >= safe[0] and i <= safe[1]:
                # print(f"{i} blocked")
                blocked = True
        if not blocked:
            iter_.append(i)
    return iter_


def struct_actual_lines(struct_in: dict, name: str) -> list:
    """returns an iterable with only the statement relative to this part
    excluding contained parts.

    WARNING:The -1 on statements is systematic because statements numbering is starting at 1
    """
    data = struct_in[name]
    safes = []
    for sub_name in data["contains"]:
        try:
            safes.append(
                [
                    struct_in[sub_name]["statements"][0] - 1,
                    struct_in[sub_name]["statements"][1] - 1,
                ]
            )
        except KeyError:
            msgerr = f"Item {sub_name} is not referenced in this context"
            raise RuntimeError(msgerr)

    return _strip_safe_lines(
        data["statements"][0] - 1, data["statements"][1] - 1, safes
    )


def struct_augment(
    struct_in: dict,
    clean_code: List[str],
    find_callables: Callable,
    compute_complexities: Callable,
    compute_cst: Callable,
) -> dict:
    """Complete the description of each struct item"""
    struct = deepcopy(struct_in)
    # first lines computation
    for _, data in struct.items():
        data["NLOC"] = data["lines"][-1] - data["lines"][0] + 1
        data["ssize"] = data["statements"][-1] - data["statements"][0] + 1

    # add internal links
    for part, data in struct.items():
        path = data["path"]
        # logger.warning(path)

        if len(path) > 1:
            parent = path[:-1] + path[-1].split(".")[:-1]
            try:
                struct[list2pathref(parent)]["contains"].append(list2pathref(path))
                # pass
            except KeyError:
                pass
                # will happen for scripts, with "dummy" not always referenced.
            # struct[part]["parents"].append(list2pathref(parent))
        # else:
        #     struct[part]["parent"]=None

    # add language specific analyses
    for part, data in struct.items():
        actual_lines = struct_actual_lines(struct, part)
        
        if actual_lines == [-1]: 
            sub_code=[""] #No code found
        elif len(clean_code) == 0:
            sub_code=[""] #No code found
        else:
            sub_code = [clean_code[i] for i in actual_lines]
            sub_code = [line for line in sub_code if line != ""] # remove void lines
            
       # logger.critical(part)
        # for i,line in enumerate(clean_code):
        #     if i  in actual_lines:
        #         logger.success(line)
        #     else:
        #         logger.warning(line)

        sub_tokenized_code = [tokenize(line) for line in sub_code]
        sub_indents_code=  [ len(get_indent(line)) for line in sub_code]

        data["weight"] = len(sub_code)
        data["callables"].extend(find_callables(sub_tokenized_code[1:]))
        if data["parents"]:
            data["callables"] = replace_self(data["callables"], data["parents"][0])
        if data["type"] in ["class"]:
            data["contains"] = replace_self(data["contains"], part)
            data["callables"] = replace_self(data["callables"], part)

        #default
        avg_indent=0
        mccabe=0
        loops=0
        #possible_paths=1
        volume=0
        difficulty=0
        time_to_code=0
        if sub_tokenized_code: # if there is some code to analyze (sometimes null)
            try:
                avg_indent,mccabe,loops,volume, difficulty,time_to_code=compute_complexities(sub_indents_code,sub_tokenized_code)
            except ZeroDivisionError: # No code to parse
                pass
        data["CCN"] = mccabe
        data["LPS"] = loops
        data["IDT"] = avg_indent
        #data["CPP"] = possible_paths
        data["HDF"] = difficulty
        data["HTM"] = time_to_code
        data["CST"] = compute_cst(data["type"])
        data["MI"] = maintainability_index(volume,mccabe, data["ssize"])

    struct = struct_aggregate(struct)


    return struct

def struct_aggregate(struct:dict)-> dict:
    """Compute recursively the averaging and sum of quantities"""
    
    def recursive_aggregate(struct:dict, label:str)-> dict:
        """Recursive summing and averaging"""
        if "aggregated" not in struct[label]:
            sums_ext = {field:struct[label][field] for field in FIELDS_EXTENSIVE}
            sums_weights = struct[label]["weight"]
            sums_int = {field:struct[label][field]*struct[label]["weight"] for field in FIELDS_INTENSIVE}
            
            for child in struct[label]["contains"]:    
                recursive_aggregate(struct, child)
                sums_ext = {field: sums_ext[field]+struct[child][field+"_ext"] for field in FIELDS_EXTENSIVE}
                sums_int = {field: sums_int[field]+struct[child][field+"_int"]*struct[child]["ssize"]  for field in FIELDS_INTENSIVE}
                sums_weights += struct[child]["ssize"]

            for field in FIELDS_EXTENSIVE:
                struct[label][field+"_ext"]= sums_ext[field]
            for field in FIELDS_INTENSIVE:
                struct[label][field+"_int"]= round((sums_int[field])/sums_weights ,2)

            struct[label]["aggregated"]=True
      
    for part in struct.keys():
        recursive_aggregate(struct, part)
    
    return struct

def aggregate_folder_struct(repo_tree, files_struct):
    def _rec_aggregate_folder( item):
        out={
            "name" : item["name"],
            "path" : item["relpath"],
            "children": []
        }
            
        if item["type"] =="file":
            try:
                data =  files_struct[item["relpath"]][item["name"].split(".")[0]]
                reduced_ext = {field:data[field+"_ext"] for field in FIELDS_EXTENSIVE}
                reduced_int = {field:data[field+"_int"] for field in FIELDS_INTENSIVE}
                reduced_sizes = {field:data[field] for field in FIELDS_SIZES}
                return out | reduced_ext | reduced_int | reduced_sizes # merge 3 dicts...
            except KeyError: 
                return None 

        else:
            sums_ext = {field:0 for field in FIELDS_EXTENSIVE+FIELDS_SIZES}
            sums_int = {field:0 for field in FIELDS_INTENSIVE}
            for subitem in item["children"]:
                data =  _rec_aggregate_folder(subitem)
                if data is None:
                    continue
                out["children"].append(data)
                sums_ext = {field: sums_ext[field]+data[field]  for field in FIELDS_EXTENSIVE+FIELDS_SIZES}
                sums_int = {field: sums_int[field]+data[field]*data["ssize"]  for field in FIELDS_INTENSIVE}
            for field in FIELDS_EXTENSIVE+FIELDS_SIZES:
                out[field]= sums_ext[field]
            for field in FIELDS_INTENSIVE:
                out[field]= round(sums_int[field] /(out["ssize"]+EPSILON),2)
            return out
        
    return _rec_aggregate_folder(repo_tree)