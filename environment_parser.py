# python 3
# an environmet data parser 
from pathlib import Path

# should be a vid path to file with data
def parseFromFile(path_to_data):
    # open and read file
    with path_to_data.open() as f:
        line = f.readline()
        lines_count = 1
        while line:
            print("Line: {}: {}".format(lines_count, line))
            line = f.readline()
            lines_count += 1 


    return None

def __checkObj():
    return None
