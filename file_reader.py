'''
This file contain different functions to read finite state machines configuration
'''
import re
import os

"""
Reads an automaton configuration file

Attributes
-------------------
path_file : an string with the path and file name of the automaton configuration file
regular_expression_list : a list with the regular expression used for parsing the automaton configuration file

Returns
-------------------
automata_tuple: a dictionary with the information obtained from the automaton configuration file. The "key" value
                corresponds to the variable name, and the "value" to the information of each variable.
"""


def read_turing_machine_config_file(path_file, regular_expression_list):
    assert path_file != "", "Path file empty!!!"
    assert os.path.isfile(path_file), "File not found!!!"
    assert regular_expression_list, "Regular expression definition missing!!!"
    turing_machine_tuple = {}
    file = open(path_file)
    lines = ','.join(file.readlines())

    for regular_expression in regular_expression_list:
        pattern = re.compile(regular_expression)
        match_obj = pattern.search(lines)
        assert match_obj, "Problems parsing the regular expression: " + regular_expression + \
                          ". It does not corresponds to the automaton definition: " + path_file
        key = match_obj.group(1)
        value = match_obj.group(2)
        match_obj = re.match("\{(.+)\}", value)
        if match_obj:
            turing_machine_tuple[key] = match_obj.group(1).split(",")
        else:
            turing_machine_tuple[key] = value
    file.close()

    return turing_machine_tuple


def read_automaton_config_file(path_file, regular_expression_list):
    assert path_file != "", "Path file empty!!!"
    assert os.path.isfile(path_file), "File not found!!!"
    assert regular_expression_list, "Regular expression definition missing!!!"
    automata_tuple = {}
    file = open(path_file)
    lines = ','.join(file.readlines())

    for regular_expression in regular_expression_list:
        pattern = re.compile(regular_expression)
        match_obj = pattern.search(lines)
        assert match_obj, "Problems parsing the regular expression: " + regular_expression + \
                          ". It does not corresponds to the automaton definition: " + path_file
        key = match_obj.group(1)
        value = match_obj.group(2)
        match_obj = re.match("\{(.+)\}", value)
        if match_obj:
            automata_tuple[key] = match_obj.group(1).split(",")
        else:
            automata_tuple[key] = value
    file.close()

    return automata_tuple
