interesting_variable = []
not_a_interesting_variable = []

source_var_a = True
source_var_b = False
source_var_c = 26

if not source_var_b:
    if source_var_c > 0:
        interesting_variable.append('Add a value')
    else:
        interesting_variable.append('otherwise add this value')
        not_a_interesting_variable.append('This value will not be observed')

    if source_var_a and source_var_c < 30:
        interesting_variable.append('This condition is relevant')
    else:
        not_a_interesting_variable.append('This condition is irrelevant')

