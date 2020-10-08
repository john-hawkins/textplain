# -*- coding: utf-8 -*-
import datetime as dt
import pkg_resources
import pandas as pd 
import numpy as np
import sys
import os

"""
    textplainer.process: Support functions for the textplainer package.
"""
########################################################################################
resource_package = __name__


########################################################################################
"""
   This is a set of functions to allow the application to print time profiles of processes
"""

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

profiles = {}

def initialise_profile():
    profiles = {}

def start_profile(proc_name):
    n1=dt.datetime.now()
    if proc_name in profiles:
        profiles[proc_name]["start"] = n1
    else:
        profiles[proc_name] = {"start":n1}

def end_profile(proc_name):
    n2 = dt.datetime.now()
    n1 = profiles[proc_name]["start"]
    total = n2-n1
    profiles[proc_name]["end"] = n2
    if "total" in profiles[proc_name]:
        curr_total = profiles[proc_name]["total"]
        profiles[proc_name]["total"] = curr_total + total
    else:
        profiles[proc_name]["total"] = total

def print_profiles():
    eprint("Computation Time Profile")
    eprint("---------------------------------------------")
    for k in profiles.keys():
        eprint(padded(k), str(profiles[k]["total"]) ) 

def padded(k):
    spacer_len = 20 - len(k)
    return k + (" "*spacer_len)

