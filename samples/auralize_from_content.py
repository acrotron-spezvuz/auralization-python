# python 3
# is an exmple of using library methods 

import sys
# import naf library
from client.nafServiceClient import nafClient
from pathlib import Path

def auralize_from_content():
    # parameter should be a valid path to the file with prepared data
    # check
    # first one is current script filename
    # second one should be a file name 
    if len(sys.argv) < 2:
        print('Path to environment data is required as an argument.')
        raise Exception("Usage: python auralize_from_content.py <file_name>")

    path_to_data = Path(sys.argv[1])

    # if path not exist or it is not a file
    if path_to_data.exists() is False or path_to_data.is_file() is False:
        print('Path to environment data is required as an argument.')
        raise Exception("Usage: python auralize_from_content.py <file_name>")

    # read all data
    content = ""
    with Path(path_to_data).open() as f:
        content = f.read()
        
    # send
    naf_client = nafClient()
    auralization_result = naf_client.auralize_from_content2(content)

    print(auralization_result)


if __name__ == "__main__":
    auralize_from_content()