from loguru import logger
from typing import List, Tuple
from math import log2,sqrt

OPERATORS_COMMON = [
    '"',",",
    "(","[","{",
    ",",".",":",";",
    "+","/","-","*","=",
    "==","!=",">",">=","<","<=",
    "*=","+=","-=","/=",
    "&"]

OPERATORS_HIDDEN = [
    ')',"]","}"
   ]
EPS=1e-12
# def show_freqs(list):
#     #my_list = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']

#     # Create an empty dictionary to store frequencies
#     freq = {}

#     # Count the occurrences of each item
#     for item in list:
#         if item in freq:
#             freq[item] += 1
#         else:
#             freq[item] = 1

#     # Print the frequencies
#     for item, count in freq.items():
#         print(f'{item}: {count}')


def halstead_numbers(code: List[List[str]], intrinsics: List[str])-> Tuple[int,int,int,int]:
    """THis takes a list of tokenized code lines"""
    operators = [] 
    operands = [] 
    for line in code:
        for token in line:
            if token in OPERATORS_HIDDEN:
                continue
            elif token in intrinsics+OPERATORS_COMMON:
                operators.append(token)
            else:
                operands.append(token)
    # show_freqs(operators)
    # print("====", len(operators))
    # show_freqs(operands)
    # print("====", len(operands))
    
    unique_operators = set(operators)
    
    unique_operands = set(operands)
    #logger.info(sorted(unique_operators))
    #logger.info(sorted(unique_operands))
    return len(operators),len(operands),len(unique_operators),len(unique_operands)

def halstead_properties(optr_tot:int,oprd_tot:int,optr_set:int,oprd_set:int)-> Tuple[int,int,int,int]:
    """ see https://en.wikipedia.org/wiki/Halstead_complexity_measures
    """
    
    # print(optr_tot,oprd_tot,optr_set,oprd_set)
    
    length = optr_tot+oprd_tot
    vocabulary= optr_set+oprd_set
    #cal_est_prog_len = oprd_set*log(oprd_set)+oprd_set*log(oprd_set)
    volume = length*log2(vocabulary+EPS)
    difficulty=optr_set/2 * oprd_tot/(oprd_set+EPS)
    effort=volume*difficulty
    # print("vocabulary:",length)
    # print("length:",length)
    # print("volume:",volume)
    # print("difficulty:",volume)
    # print("effort:",volume)
    
    return round(volume,2), round(difficulty,2), round(effort,2)


def count_ctrl_pts(code: List[list], ctl_pts:List[str]):
    """Count the nb of occurences of control pts in a tokenized code"""
    counts = 0
    for line in code:
        for token in line:
            if token in ctl_pts:
                counts += 1
    return counts


def compute_control_pts(control_points,active_ctl_pts:list,passive_ctl_pts:list):
    """
    Computes the cyclomatic complexity based on nested list control points.

    Args:
        control_points (list): A nested list representing control flow points.

    Returns:
        int: The cyclomatic complexity.
    """

    def rec_sum_control_pts(points,active_ctl_pts,passive_ctl_pts):
        complexity = 0
        for point in points:
            if isinstance(point, list):
                complexity += rec_sum_control_pts(point,active_ctl_pts,passive_ctl_pts)
            elif point in active_ctl_pts:
                complexity += 1
            elif point in passive_ctl_pts:
                pass
            else:
                logger.debug("")
                # the else is not an additional path
        return complexity

    # Start with a base complexity of 1 (one path through the code)
    base_complexity = 0
    total_complexity = base_complexity + rec_sum_control_pts(control_points,active_ctl_pts,passive_ctl_pts)
    return total_complexity


def compute_possible_paths(control_points:list,active_ctl_pts:list,passive_ctl_pts:list):
    """
    Computes the possible_paths based on nested list control points.

    Args:
        control_points (list): A nested list representing control flow points.

    Returns:
        int: The possible paths
    """
    paths = 1
    for point in control_points:
        if isinstance(point, list):
            # Recursively count paths in nested lists
            nested_paths = compute_possible_paths(point,active_ctl_pts,passive_ctl_pts)
            paths += nested_paths - 1
        elif point in active_ctl_pts:
            paths = 2 * paths
        elif point in passive_ctl_pts:
            paths += 1
        else:
            pass
    return paths

def maintainability_index(halstead_volume:float, cyclomatic_complexity:float,loc:int, pct_comment:float=0)-> float:
    """ compute the maintainability index
    https://sourcery.ai/blog/maintainability-index/
    https://www.ecs.csun.edu/~rlingard/comp589/ColemanPaper.pdf
    """
    mi = 171 - 5.2 * log2(halstead_volume+EPS) - 0.23 * cyclomatic_complexity - 16.2 * log2(loc) + 50 * sqrt(2.46 * pct_comment)
#    return round(mi/3.7806,2)/ Limit to 100 for a void file
    return round(mi,2)
