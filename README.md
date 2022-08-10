# FSMTools
library for creating finite state machines in python

# Use

detailed description coming soon. 

To see a demo of the library, just run FSMTools.py with no arguments.

Basically, if you have an FSM design with n states, m inputs, and p transitions, you can create a text file that describes your state machine in the format:

```
state_1_name,state_2_name,...,state_n_name
input_1_name,input_2_name,...,input_m_name
transition_1_initial_state,transition_1_condition,transition_1_final_state
transition_2_initial_state,transition_2_condition,transition_2_final_state
...
transition_p_initial_state,transition_p_condition,transition_p_final_state
```
The conditions in each transition should each resolve to a Boolean and be written in Python language using the state and input names you defined. The FSM object will take a list of Booleans, one for each of your defined inputs, and calculate the current machine state.

Then, you can create a FSM object by calling:

```python
from FSMTools import FSM,State,Transition
mymachine = FSM()
filename = "my_fsm_text_file.txt"
mymachine.loadFromTXT(filename)
```

Then, in an infinite loop or some other repetitive structure, you can call

```python
#your inputs could come from anywhere-- timers, counters, buttons...
inputs = [False, True, ... False]
mymachine.update(inputs)

#to print the current machine state, call debugPrint() method
mymachine.debugPrint()

#to just see what state you're in, call currentState member:
print(mymachine.currentState)
```
