# -*- coding: utf-8 -*-
 
""" 
   textplainer.cli: provides entry point main()
"""

import pandas as pd
import sys
import os

from .explain import explain_predictions

def main():
    if len(sys.argv) < 2:
        print("ERROR: MISSING ARGUMENTS")
        print_usage(sys.argv)
        exit(1)
    else:
        params = get_cmd_line_params(sys.argv)

        if not os.path.exists(params["model"]):
            print("ERROR: Model to test does not exist")
            print_usage(sys.argv)
            exit(1)

        if not os.path.exists(params["dataset"]):
            print("ERROR: Testing data does not exist")
            print_usage(sys.argv)
            exit(1)

        rez = explain_predictions(params["model"], params["dataset"], params["column"], params)

        print(rez)


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
    data = argv[-1]
    column = argv[-2]
    model = argv[-3]
    options = argv[1:-3]
    result = {"dataset":data,
              "column":column, 
              "model":model 
    }

    return result

#############################################################
def print_usage(args):
    """ Command line application usage instrutions. """
    print("USAGE ")
    print(args[0], " [ARGS] <PATH TO SERLIALISED MODEL> <TEXT COLUMN NAME> <PATH TO TEST DATA>")
    print("  <PATH TO MODEL>   - Pickled model that adheres to the Interface.")
    print("  <COLUMN NAME>     - Name of the column that containts text data.")
    print("  <PATH TO DATA>    - Path to a dataset to explain the text value contribution.")
    print("")


