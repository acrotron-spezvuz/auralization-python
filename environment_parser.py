# python 3
# an environmet data parser 
from pathlib import Path
from environment import Environment, SourceFrame, Reciever, Source
import re

# should be a vid path to file with data
def parse_from_path(path_to_data: Path) -> Environment:
    # open and read file
    env = Environment()
    with path_to_data.open() as f:
        source_frames = {}
        recievers = {}
        # a representation of relationships of source frames and sources 
        sources_map = {}

        line = f.readline()
        skip_to_struct_end = False
        while line:
            line = line.strip()
            #print("Line: {}: {}".format(lines_count, line))
            
            if line is not "end" and skip_to_struct_end is False:
                if __startswith(line, "sourceframes"):
                    # split line into a list by space separator 
                    lst = line.split()
                    # get sourceframes ids if array contains more than keyword
                    if len(lst) > 1: 
                        # fill dict with keys and empty values
                        source_frames = __map_list_to_empty_dict(lst)
                elif __startswith(line, "sourceframe"):
                    # get source frame by name 
                    lst = line.split()
                    # skip source if it is not in list
                    if len(lst) > 1 and lst[1] in source_frames:
                        sf = SourceFrame()
                        sf.id = lst[1]
                        # assign
                        source_frames[lst[1]] = sf
                    
                elif __startswith(line, "source"):
                    pass
                elif __startswith(line, "components"):
                    pass
                elif __startswith(line, "component"):
                    pass
                elif __startswith(line, "receivers"):
                    lst = line.split()
                    if len(lst) > 1:
                        recievers = __map_list_to_empty_dict(lst)
                    pass
                elif __startswith(line, "receiver"):
                    # add reciever
                    lst = line.split()
                    if len(lst) > 1 and lst[1] in recievers:
                        reciever = Reciever()
                        reciever.id = lst[1]
                        recievers[lst[1]] = reciever
                else:
                    print("How to parse the line? : ", line)

            line = f.readline()
            
        # all lines are parsed 
        # map source frames
        env.source_frames = [source_frames[key] for key in source_frames]
        # map recievers
        env.recievers = [recievers[key] for key in recievers]
    return env

def __startswith(line: str, pattern: str) -> bool:
    return bool(re.match(pattern, line, re.I))

def __map_list_to_empty_dict(the_list: list) -> dict:
    return { item:None for item in the_list[1:len(the_list)] } 