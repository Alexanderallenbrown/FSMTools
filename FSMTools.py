class State:
    def __init__(self,name):
        self.name=name
        self.value=False

class Transition:
    def __init__(self,initial,exprn,final):
        self.initial = initial
        self.final = final
        self.exprn = exprn
        self.value = False

class FSM:
    def __init__(self):
        #list of state objects
        self.states = []
        #list of transition objects
        self.transitions = []
        #list of input names
        self.inputNames = []
        #current index of the machine state
        self.currentState = None

    def debugPrint(self):
        print("FSM Summary: current state is "+str(self.currentState))
        for k in range(0,len(self.states)):
            print("state "+self.states[k].name+" is "+str(self.states[k].value))
        for k in range(0,len(self.transitions)):
            print("transition: "+str([self.transitions[k].initial,self.transitions[k].exprn,self.transitions[k].final])+"; truth value: "+str(self.transitions[k].value))

    def loadFromTxt(self,fileName):
        #open the text file
        file = open(fileName,'r')
        #separate the file into lines
        fileLines = list(file)
        #first line should be states separated by comma
        states = fileLines[0].strip()
        states = states.split(",")
        for k in range(0,len(states)):
            #create a state object for each name in the list
            self.states.append(State(states[k]))
        #initialize state to the first one:
        self.states[0].value = True
        #second line should be inputs
        inputs = fileLines[1].strip()
        inputs = inputs.split(",")
        self.inputNames = inputs
        #remaining lines should be transitions
        #format is starting_state,condition,ending_state
        for k in range(2,len(fileLines)):
            #strip newlines
            transition_stripped = fileLines[k].strip()
            #split into from,exprn,to
            transition_split = transition_stripped.split(",")
            #now create a transition object and append
            self.transitions.append(Transition(transition_split[0],transition_split[1],transition_split[2]))

    def update(self,inputs):
        #assert(len(inputs)==len(self.inputNames),"number of inputs is incorrect!")
        #create local variables for all input names
        for k in range(0,len(inputs)):
            #create a line of code that creates the input variables
            inputstring = self.inputNames[k]+"="+str(inputs[k])
            #print("input command: "+str(inputstring))
            exec(inputstring)
        #create local variables for all FSM state truth variables
        for k in range(0,len(self.states)):
            exec(self.states[k].name+"="+str(self.states[k].value))
        #evaluate each transition (block 2)
        for k in range(0,len(self.transitions)):
            #evaluate the expresion in each transition
            self.transitions[k].value = eval(self.transitions[k].initial+" and "+self.transitions[k].exprn)
        #evaluate truth value of each state (block 3)
        for j in range(0,len(self.states)):
            #first reset all state truths to False so we can do a true "or" on all transitions
            self.states[j].value=False
            for k in range(0,len(self.transitions)):
                #if this transition ends at this state, add it to the "or" statement
                if self.transitions[k].final==self.states[j].name:
                    #this will set this state to True if any of its transitions are true.
                    self.states[j].value = self.states[j].value or self.transitions[k].value
        statesum = 0
        for j in range(0,len(self.states)):
            if self.states[j].value:
                self.currentState=self.states[j].name
                statesum+=1
        if(statesum==0):
            print("error: you have fallen through logic and no states are true!")
        elif(statesum>1):
            print("error: you have fallen through logic and are in more than one state!")


def demo():
    #demonstrate the FSM class
    #first create a text file that defines the fsm.
    #normally you'd do this separately.
    fileContents ="""state_A,state_B
    btn_prs
    state_A,btn_prs,state_B
    state_A,not(btn_prs),state_A
    state_B,btn_prs,state_A
    state_B,not(btn_prs),state_B"""
    #write this definition to a file. normally this would be done separately
    machineFile = open("fsm_definition.txt","w")
    machineFile.write(fileContents)
    machineFile.close()
    #now create an FSM object
    fsm = FSM()
    #use the loadFromTxt method to load our FSM
    fsm.loadFromTxt("fsm_definition.txt")
    fsm.debugPrint()
    #now we can test this FSM! We will use a continuous loop

    while True:
        inp = input("value of btn_prs (True or False) or q to quit:    ")
        if inp == 'q':
            break
        if(inp=="True"):
            btn_prs = True
        elif(inp=="False"):
            btn_prs=False
        else:
            print("invalid input, setting input to false:")
            btn_prs = False
        #send our input to the FSM, update it
        fsm.update([btn_prs])
        #now use the debugPrint method of the FSM to see what happened
        fsm.debugPrint()


if __name__=='__main__':
    demo()
