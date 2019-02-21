import file_reader
import finite_state_machine


def main():
    automaton_regular_expression_list = ["@(sigma)=(\{[\w|,]+\})", "@(Q)=(\{[\w,]+\})", "@(f)=(\{(([\(\w\s\)]+->\w+)|,)+\})",
                                         "@(q0)=(\w+)", "@(F)=(\{([\w,]+)+\})", "@(test)=(\{[\w,]+\})"]
    automaton_tuple = file_reader.read_automaton_config_file('automata_definitions/automata_correct.def', automaton_regular_expression_list)
    assert automaton_tuple is not None, "Problems reading the config file!"
    transition_function_dictionary = finite_state_machine.build_automaton_model(automaton_tuple, "F", "Q", "q0", "f",
                                                                                "sigma")
    assert transition_function_dictionary is not None, "Problems building the model!"
    results = finite_state_machine.test_automaton_model(transition_function_dictionary, automaton_tuple["test"], automaton_tuple["q0"], automaton_tuple["F"])
    if results:
        for result in results:
            print(result, results[result])


if __name__ == "__main__":
    main()
