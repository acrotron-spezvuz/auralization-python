# python 3
# an environmet data parser 
from pathlib import Path
from environment import Environment, SourceFrame, Reciever, Source, Component
import re

# should be a vid path to file with data
def parse_from_path(path_to_data: Path) -> Environment:
    # open and read file
    env = Environment()
    with path_to_data.open() as f:
        source_frames = {}
        recievers = {}
        source_map = {}
        sources = {}
        components = {}
        sinks = {}

        line = f.readline()
        # skip_to_struct_end = False
        while line:
            line = line.strip()
            
            if __startswith(line, "end") or len(line) is 0:
                line = f.readline()
                continue
                
            # awesome switch ... case
            if __startswith(line, "sourceframes"):
                # split line into a list by space separator 
                # fill dict with keys and empty values
                source_frames = __parse_line_with_names(line)
            
            elif __startswith(line, "sourceframe"):
                # get source frame by name 
                lst = line.split()
                # skip source if it is not in list
                if len(lst) > 1 and lst[1] in source_frames:
                    sf = SourceFrame()
                    sf.id = lst[1]
                    source_frames[lst[1]] = sf
            
            elif __startswith(line, "sources"):
                source_map = __parse_line_with_names(line)
            
            elif __startswith(line, "source"):
                lst = line.split()
                if len(lst) > 1 and lst[1] in source_map:
                    source = Source()
                    source.id = lst[1]
                    sources[lst[1]] = source

            elif __startswith(line, "components"):
                components = __parse_line_with_names(line)
            
            elif __startswith(line, "component"):
                lst = line.split()
                if len(lst) > 1 and lst[1] in components:
                    component = Component()
                    component.id = lst[1]
                    components[lst[1]] = component
            
            elif __startswith(line, "receivers"):
                recievers = __parse_line_with_names(line)
            
            elif __startswith(line, "receiver"):
                # add reciever
                lst = line.split()
                if len(lst) > 1 and lst[1] in recievers:
                    reciever = Reciever()
                    reciever.id = lst[1]
                    recievers[lst[1]] = reciever

            elif __startswith(line, "sinks"):
                sinks = __parse_line_with_names(line)

            elif __startswith(line, "sink"):
                pass
            elif __startswith(line, "traj"):
                pass
            else:
                print("How to parse the line? : ", len(line), line)

            line = f.readline()
            
        # all lines are parsed 
        # map source frames
        env.source_frames = [source_frames[key] for key in source_frames]
        # map recievers
        env.recievers = [recievers[key] for key in recievers]
    return env

def __parse_line_with_names(line: str) -> dict:
    the_list = line.split()
    if len(the_list) > 1:
        return __map_list_to_empty_dict(the_list)
    else:
        return {}

def __startswith(line: str, pattern: str) -> bool:
    return bool(re.match(pattern, line, re.I))

def __map_list_to_empty_dict(the_list: list) -> dict:
    return { item:None for item in the_list[1:len(the_list)] } 