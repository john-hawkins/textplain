# -*- coding: utf-8 -*-
 
""" textplainer.cli: provides entry point main()."""
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
       Parse out the option from an array of command line arguments 
       and return them in a dictionary. Note: there are multiple options
       here that are not yet implemented.
    """
    data = argv[-1]
    column = argv[-2]
    model = argv[-3]
    options = argv[1:-3]
    result = {"dataset":data,
              "column":column, 
              "model":model, 
              "profanity":False, 
              "sentiment":False, 
              "traits":False, 
              "rhetoric":False, 
              "literacy":False 
    }
    for o in options:
        parts = o.split("=")
        if parts[0] == "-literacy":
            result["literacy"]=True
        if parts[0] == "-profanity":
            result["profanity"]=True
        if parts[0] == "-sentiment":
            result["sentiment"]=True
        if parts[0] == "-traits":
            result["traits"]=True
        if parts[0] == "-rhetoric":
            result["rhetoric"]=True

    return result

#############################################################
def print_usage(args):
    """ Command line application usage instrutions. """
    print("USAGE ")
    print(args[0], " [ARGS] <PATH TO PICKLE SERLIALISED MODEL> <TEXT COLUMN NAME> <PATH TO TEST DATA>")
    print("  <PATH TO PICKLE SERLIALISED MODE> - Supports models with the SciKit Learn Interface.")
    print("  <TEXT COLUMN NAME> - Name of the column that containts text data.")
    print("  <PATH TO TEST DATA> - File path to a dataset for which we need to explain the text value contribution.")
#    print(" [ARGS] Switches that turn on the explanation type")
#    print("  -profanity (Default: False) Test for the impact of profanity.")
#    print("  -sentiment (Default: False) Test for the impact of sentiment.")
    print("")


