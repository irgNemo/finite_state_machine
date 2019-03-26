import file_reader
import finite_state_machine


def main():
    turing_machine_regular_expression_list = ["@(sigma)=(\{.+\})", "@(Q)=(\{[\w,]+\})", "@(f)=(\{((\(.+\)->(\(.+\)+)|,))+\})",
                                         "@(q0)=(\w+)", "@(F)=(\{([\w,]+)+\})","@(b)=(\w)", "@(test)=(\{.+\})", "@(R)=(\{.+\})", "@(HM)=(\{.+\})"]
    turing_machine_tuple = file_reader.read_turing_machine_config_file('turing_machine_definitions/turing_machine_correct_corchetes_anidados.def',
                                                                       turing_machine_regular_expression_list)
    assert turing_machine_tuple is not None, "Problems reading the config file!"
    transition_function_dictionary = finite_state_machine.build_turing_machine_model(turing_machine_tuple, "F", "Q", "q0", "f",
                                                                                   "sigma", "R", "b", "HM", "\((.+)\s(.+)\)->\((.+)\s(.+)\s(.+)\)")
    assert transition_function_dictionary is not None, "Problems building the model!"
    results = finite_state_machine.test_turing_machine_model(transition_function_dictionary,
                                                             turing_machine_tuple["test"],
                                                             turing_machine_tuple["q0"], turing_machine_tuple["F"],
                                                             turing_machine_tuple["b"], turing_machine_tuple["sigma"])
    if results:
        for result in results:
            print(result, results[result])
    else:
        print("There are no results, bye")



if __name__ == "__main__":
    main()
