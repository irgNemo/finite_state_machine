import re
"""
Validate if the automaton model information

Attributes
-----------------
automaton_tuple: a dictionary with the automaton definition without been validated and parsed

Return
-----------------
A dictionary with the automaton information validated and in proper format to be tested
"""


def build_turing_machine_model(turing_machine_tuple, final_state_symbol, states_set_symbol, initial_state_symbol,
                          transition_function_symbol, alphabet_set_symbol, ro_set_symbol, blank_symbol):
    is_final_state = validate_final_states(turing_machine_tuple[final_state_symbol], turing_machine_tuple[states_set_symbol])
    assert is_final_state, "Final states definition is incorrect: " + final_state_symbol
    is_initial_state = validate_initial_state(turing_machine_tuple[initial_state_symbol], turing_machine_tuple[states_set_symbol])
    assert is_initial_state, "Initial state definition is incorrect: " + initial_state_symbol
    is_sigma_subset_ro = validate_sigma_in_ro(turing_machine_tuple[alphabet_set_symbol],
                                              turing_machine_tuple[ro_set_symbol])
    assert is_sigma_subset_ro, "Sigma is not a subset of ro set: " + alphabet_set_symbol + ro_set_symbol
    is_b_in_ro = validate_blank_in_ro(turing_machine_tuple[blank_symbol], turing_machine_tuple[ro_set_symbol])
    assert is_b_in_ro, "Blank symbol is not in ro set" + blank_symbol
    is_b_not_in_sigma = validate_b_not_in_sigma(turing_machine_tuple[blank_symbol],
                                                turing_machine_tuple[alphabet_set_symbol])
    assert is_b_not_in_sigma, "Blank symbol should not be a member of sigma set"
    transition_function_dictionary = transform_transition_function_to_dictionary(turing_machine_tuple[
                                                                                transition_function_symbol],
                                                                                 turing_machine_tuple[states_set_symbol],
                                                                                 turing_machine_tuple[ro_set_symbol])
    is_transition_function = validate_transition_function(transition_function_dictionary,
                                                          turing_machine_tuple[states_set_symbol],
                                                          turing_machine_tuple[ro_set_symbol])
    assert is_transition_function, "Transition function was not well constructed: " + transition_function_symbol
    return transition_function_dictionary


def build_automaton_model(automaton_tuple, final_state_symbol, states_set_symbol, initial_state_symbol,
                          transition_function_symbol, alphabet_set_symbol):
    is_final_state = validate_final_states(automaton_tuple[final_state_symbol], automaton_tuple[states_set_symbol])
    assert is_final_state, "Final states definition is incorrect: " + final_state_symbol
    is_initial_state = validate_initial_state(automaton_tuple[initial_state_symbol], automaton_tuple[states_set_symbol])
    assert is_initial_state, "Initial state definition is incorrect: " + initial_state_symbol
    transition_function_dictionary = transform_transition_function_to_dictionary(automaton_tuple[
                                                                                transition_function_symbol],
                                                                                automaton_tuple[states_set_symbol],
                                                                                automaton_tuple[alphabet_set_symbol])
    is_transition_function = validate_transition_function(transition_function_dictionary,
                                                          automaton_tuple[states_set_symbol],
                                                          automaton_tuple[alphabet_set_symbol])
    assert is_transition_function, "Transition function was not well constructed: " + transition_function_symbol

    return transition_function_dictionary


def test_turing_machine_model(transition_function_dictionary, test_language, inital_state, final_state_set, blank_symbol, alphabet_set):
    results = {}
    is_test_language_valid = validate_test_language(test_language, alphabet_set)
    assert is_test_language_valid, "The test language is not correctly builded"
    for word in test_language:
        current_state = inital_state
        character_index = 1
        word_list = list(word)
        word_list.append(blank_symbol)
        word_list.insert(0, blank_symbol)
        while True:
            next_tuple = transition_function_dictionary[current_state][word_list[character_index]]
            if (current_state in final_state_set) and (next_tuple is None):
                results[word] = word_list, "Accepted"
                break
            elif next_tuple is None:
                results[word] = word_list, "Rejected"
                break

            current_state = next_tuple[0]
            word_list[character_index] = next_tuple[1]
            if next_tuple[2] == 'R':
                character_index += 1
                if character_index >= len(word_list):
                    word_list.append(blank_symbol)
            elif next_tuple[2] == 'L':
                character_index -= 1
                if character_index < 0:
                    word_list.insert(0, blank_symbol)
                    character_index = 0

    return results


def test_automaton_model(transition_function_dictionary, test_language, inital_state, final_state_set):
    results = {}
    for word in test_language:
        current_state = inital_state
        for character in word:
            current_state = transition_function_dictionary[current_state][character]
            if current_state is None:
                results[word] = "Rejected"
                break
        results[word] = "Accepted" if current_state in final_state_set else "Rejected"
    return results


def validate_test_language(test_language, alphabet_set):
    is_valid = True
    for word in test_language:
        for letter in word:
            if letter in alphabet_set:
                is_valid = is_valid and True
            else:
                is_valid = False
                break
    return is_valid


def validate_sigma_in_ro(sigma_set, ro_set):
    is_valid = True
    for value in sigma_set:
        if value not in ro_set:
            is_valid = is_valid and False
    return is_valid


def validate_blank_in_ro(blank, ro_set):
    return blank in ro_set


def validate_b_not_in_sigma(blank, sigma_set):
    return blank not in sigma_set


def validate_final_states(final_states_set, states_set):
    is_subset = True
    for final_state in final_states_set:
        if final_state not in states_set:
            is_subset = is_subset and False
    return is_subset


def validate_initial_state(initial_state, states_set):
    return True if (initial_state in states_set) else False


def transform_transition_function_to_dictionary(transition_function_set, states_set, ro_set):
    transition_function_dictionary = {}
    for state in states_set:
        transition_function_dictionary[state] = {}
        for alphabet in ro_set:
            transition_function_dictionary[state][alphabet] = None

    pattern = re.compile("\((.+)\s(.+)\)->\((.+)\s(.+)\s(.+)\)")
    for transition_function in transition_function_set:
        transition_function = transition_function.strip()
        match_obj = pattern.match(transition_function)
        previous_state_transition_function = match_obj.group(1)
        previous_ro_value_transition_function = match_obj.group(2)
        next_state_transition_function = match_obj.group(3)
        next_ro_value_transition_function = match_obj.group(4)
        head_movement = match_obj.group(5)
        transition_function_dictionary[previous_state_transition_function][previous_ro_value_transition_function] = \
            (next_state_transition_function, next_ro_value_transition_function, head_movement)
    return transition_function_dictionary


def validate_transition_function(transition_function_dictionary, states_set, ro_set, head_movements=['R','L','S']):
    is_valid = True
    for state in transition_function_dictionary:
        is_valid = is_valid and (state in states_set)
        for ro in transition_function_dictionary[state]:
            is_valid = is_valid and ((ro in ro_set) or ro is None)
            resulting_list = transition_function_dictionary[state][ro]
            if resulting_list is not None:
                is_valid = is_valid and (((resulting_list[0] in states_set) and (resulting_list[1] in ro_set) and
                                     (resulting_list[2] in head_movements)))
            else:
                is_valid = is_valid and True
    return is_valid
