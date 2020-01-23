[pyLogicFlowChart](https://pasteboard.co/IRj0Hgq.png) "pyLogicFlowChart logo"

# pyLogicFlowChart
pyLogicFlowChart is a static analyzer that helps create a flowchart of logical conditions in python source code, which is pruned to singular `variable of interest`

## Usage
```
usage: analyzer.py [-h] [-s SOURCE] [-v VARIABLE_OF_INTEREST]
                   [-a {dict-add,list-append}] [-c]

Params for CodeLogicFlow

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Path of the target python file to visualize
  -v VARIABLE_OF_INTEREST, --variable-of-interest VARIABLE_OF_INTEREST
                        variable of interest in the given target file
  -a {dict-add,list-append}, --action-of-interest {dict-add,list-append}
                        The action of interest that the variable does
  -c, --has-self        Specifies variable of interest is a class variable
```

## Example
The following example is in `sample.py`. It can be executed by simply running the command

### Source Code:
The following code is present in `sample.py`:
```
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
```

### Command
```
python analyzer.py -s sample.py -v interesting_variable -a list-append
```

### Output
![flowchart](https://pasteboard.co/IRiUd0N.png) "Resulting Chart"

### Limitations
The tool only checks for direct changes to the variable. It will ignore instances where condition checking is done on an interim variable, whose end result is used to populate the `variable of interest`
