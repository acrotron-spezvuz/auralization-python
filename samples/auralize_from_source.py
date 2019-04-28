# python 3
# is an exmple of using library methods 

import sys
# import naf library
from client.nafServiceClient import nafClient
from pathlib import Path
import json

if __name__ == "__main__":
    # parameter should be a valid path to the file with prepared data
    # check
    # first one is current script filename
    # second one should be a file name 
    if len(sys.argv) < 2:
        raise Exception('path to file required')

    path_to_data = Path(sys.argv[1])

    # if path not exist or it is not a file
    if path_to_data.exists() is False or path_to_data.is_file() is False:
        raise Exception('path to file required')

    # read all data
    file_data = ""
    with path_to_data.open() as f:
        file_data = f.read()

    # parse 
    data_obj = json.loads(file_data)

    # send
    naf_client = nafClient()
    auralization_result = naf_client.auralize_from_sources(data_obj)

    print(auralization_result)
