# -*- coding: utf-8 -*-
import sys
import os

"""
    textplainer.utils: Support functions for the textplainer package.
"""

def eprint(*args, **kwargs):
    """
    Wrapper function for printing to STDERR
    """
    print(*args, file=sys.stderr, **kwargs)

def get_coloured_text_string(text, colour):
    """
    Wrap a string with some unicode to colour it in the terminal.

    :param text: The text block that we want to explain.
    :type text: string, required

    :param colour: The name of the colour you want encoded 
    :type colour: string, required

    :return: The colour encoded text
    :rtype: string
    """
    if colour=="red":
        return ("\033[31m" + text + "\033[0m")
    if colour=="green":
        return ("\033[32m" + text + "\033[0m")
    if colour=="yellow":
        return ("\033[33m" + text + "\033[0m")
    if colour=="blue":
        return ("\033[34m" + text + "\033[0m")
    if colour=="purple":
        return ("\033[35m" + text + "\033[0m")
    if colour=="cyan":
        return ("\033[36m" + text + "\033[0m")
    if colour=="white":
        return ("\033[37m" + text + "\033[0m")
    return text



