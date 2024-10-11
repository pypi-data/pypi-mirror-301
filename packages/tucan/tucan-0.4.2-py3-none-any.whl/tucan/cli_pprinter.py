

from  tucan.struct_common import FIELDS_EXT_DICT,FIELDS_INT_DICT,FIELDS_SIZES_DICT

EPSILON=1e-14
def struct_summary_file(file_struct: dict) -> str:
    out = []

    if file_struct is None:
        return "No structure data is available. Tucan light parser could not interpret this file."
    for part, data in file_struct.items():
        out.append(f'\n{data["type"]} {part} :')
        out.append(
            f'    At path {data["path"]}, name {data["name"]}, lines {data["lines"][0]} -> {data["lines"][-1]}'
        )

        for field, legend in FIELDS_SIZES_DICT.items():
            out.append(f'    {legend}  {data[field]}')
        for field, legend in FIELDS_INT_DICT.items():
            value = show_value(data[field])
            value2 =show_value(data[f'{field}_int'])
            out.append(f'    {legend}  {value} | {value2} Int. avg.')
        for field, legend in FIELDS_EXT_DICT.items():
            if field in ["HTM"] :
                value = show_time(data[field])
                value2 =  show_time(data[f"{field}_ext"])
            else:
                value = show_value(data[field])
                value2 =show_value(data[f'{field}_ext'])
            out.append(f'    {legend}  {value} | {value2} Ext. avg.')
        
        for content in ["callables","contains","parents","annotations"]:
            if data[content]:
                list_str = "\n       - " + "\n       - ".join(data[content])
                out.append(f'    Refers to {len(data[content])} {content}:{list_str}')

    return "\n".join(out)



def struct_summary_repo(repo_structs: dict, depth:int=2) -> str:
    
    def _rec_print(item, lvl:int=1):
        out=[]
        indent="   |"*lvl
        previndent="   |"*(lvl-1)
        
        
        if lvl < depth:
            out.append(f'{previndent}')
            for child in item["children"]:
                out.extend(_rec_print(child, lvl+1))
                out.append(f'{indent}===*')
                

        out.append(f'{indent}')
        out.append(indent+" Name:"+item["name"])
        out.append(indent+" Path:"+item["path"])
        for field, legend in FIELDS_SIZES_DICT.items():
            value = show_value(item[field])
            out.append(f'{indent} {value}   sum of {legend}  ')
        for field, legend in FIELDS_EXT_DICT.items():
            if field in ["HTM"] :
                value = show_time(item[field])
            else:
                value = show_value(item[field])
            out.append(f'{indent} {value} {legend} (agregated sum)')
        
        value = show_time(50*item["HTM"]/(item["NLOC"]+EPSILON))
        out.append(f'{indent} {value} for 50 lines of code')

        for field, legend in FIELDS_INT_DICT.items():
            value = show_value(item[field])
            out.append(f'{indent} {value} {legend} (averaged per procedure)')
        return out
    
    all_str = _rec_print(repo_structs)
    return "\n".join(all_str)


def show_value(val)->str:
    if isinstance(val, (int, float)):
        val =  f"{val:.10g}"
    return str(val).ljust(10)

def show_time(timesec:int)->str:
    out = str(round(timesec,2)) + " sec"
    if timesec >= 60:
        out = f"{round(timesec*1./60,2)} min"
    if timesec >= 3600:
        out = f"{round(timesec*1./3600,2)} hrs"
    if timesec >= 3600*24:
        out = f"{round(timesec*1./(3600*24),2)} dys"
    if timesec >= 3600*24*364.2422:
        out = f"{round(timesec*1./(3600*24*364.2422),2)} yrs"

    return show_value(out)

