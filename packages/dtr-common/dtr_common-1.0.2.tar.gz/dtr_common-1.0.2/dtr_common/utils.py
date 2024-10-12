from copy import deepcopy
from typing import cast

def parse_params(params: dict[str, str]) -> dict[str, str | int | bool]:
    """
    this function parse query parameters
    """
    new_params = deepcopy(params)
    for key, value in new_params.items():
        if value.lower() in ("true", "false"):
            new_params[key] = True if value.lower() == "true" else False  # type: ignore
        elif value.isdigit():
            new_params[key] = int(value)  # type: ignore
    return cast(dict[str, str | int | bool], new_params)

def dest_path_renaming(root_path: str, dest_path: str, filename: str,
                       tmp_prefix_dest: str, final_prefix_dest: str) -> str:
    
    """
        Ths fuction aims is to rename the destination path with prefixes if exists
    """
    if dest_path is not None:

        if tmp_prefix_dest is not None and final_prefix_dest is not None:
            dest_path = dest_path.replace(tmp_prefix_dest, final_prefix_dest, 1)
        elif final_prefix_dest is not None and tmp_prefix_dest is None:
            dest_path = f"{root_path}/{final_prefix_dest}{filename}" if root_path is not None else final_prefix_dest + filename
        elif final_prefix_dest is None and tmp_prefix_dest is not None:
            dest_path = dest_path.replace(tmp_prefix_dest, "", 1)
        else:
            pass  
    return dest_path
