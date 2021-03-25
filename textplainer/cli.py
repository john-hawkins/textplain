# -*- coding: utf-8 -*-
 
""" 
   textplainer.cli: provides entry point main()
"""

import pandas as pd
import sys
import os

from .models import load_and_test_model
from .explain import explain

def main():
    """
    Main function is the entry point for the command line application.
    It expects to find the required parameters in ```sys.argv```
    """
    if len(sys.argv) < 4:
        print("ERROR: MISSING ARGUMENTS")
        print_usage(sys.argv)
        exit(1)
    else:
        params = get_cmd_line_params(sys.argv)

        if not os.path.exists(params["model"]):
            print("ERROR: Model to test does not exist")
            print_usage(sys.argv)
            exit(1)

        if not os.path.exists(params["src"]):
            print("ERROR: Path to src code does not exist")
            print_usage(sys.argv)
            exit(1)

        if not os.path.exists(params["dataset"]):
            print("ERROR: Testing data does not exist")
            print_usage(sys.argv)
            exit(1)

        try:
            rez = explain(params["model"], 
                          params["src"],
                          params["dataset"], 
                          params["column"], params)
            print(rez)

        except Exception as err:
            print(err)


#############################################################
def get_cmd_line_params(argv):
    """ 
    Function to parse out the options and parameters from an array of 
    command line arguments and return them in a dictionary. 
    Note: there are multiple options here that are not yet implemented.

    TODO: Switch and use a standard argument parsing library.

    :param argv: The array of command line arguments recieved by the app
    :type argv: Array(String), required

    :returns: A dictionary of required values
    :rtye: Dictionary
    """
    column = argv[-1]
    data = argv[-2]
    src = argv[-3]
    model = argv[-4]
    options = argv[1:-4]
    result = {"dataset":data,
              "column":column, 
              "model":model,
              "src":src 
    }

    return result

#############################################################
def print_usage(args):
    """ 
    Print out the command line application usage instructions. 

    :returns: Null
    :rtye: Null
    """
    print("USAGE ")
    print(args[0], " [ARGS] <MODEL> <SRC> <DATA> <COLUMN>")
    print("  <MODEL>   - Path to the pickled model. *")
    print("  <SRC>     - Path to the src code for the model. ^")
    print("  <DATA>    - Path to a dataset to be explained.")
    print("  <COLUMN>  - Name of the column that contains text data.")
    print("")
    print("NOTES: ")
    print("  * Model must adhere to the interface defined in ModelInterface.py")
    print("  ^ Must be a path to a directory of source code with __init__.py")



