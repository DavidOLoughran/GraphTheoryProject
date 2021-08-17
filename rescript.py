
import argparse

# Psuedo code used for shunt(infix) found at https://en.wikipedia.org/wiki/Shunting-yard_algorithm


def shunt(infix):
    """Convert infix expressions to postfix."""
    # Postfix will be the output.
    postfix = ""
    # The shunting yard operator stack.
    stack = ""
    # Order of Operators.
    prec = {'*': 100, '.': 90, '|': 80}
    # Loop through the input a character at a time.
    for c in infix:
        # If see is an operator.
        if c in {'*', '.', '|'}:
            # Check what is on the stack and Add operator to the top of the stack for the output
            #Then remove operator from the stack
            while len(stack) > 0 and stack[-1] != '(' and prec[stack[-1]] >= prec[c]:
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            # Adds c to the stack.
            stack = stack + c
        elif c == '(':
            stack = stack + c
        elif c == ')':
            while stack[-1] != "(":
                # Add operator to top of stack to be outputted
                # Then remove the operator and open bracket from the stack.
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            stack = stack[:-1]
                
        # if c is a literal character/number add it to the output .
        else:
            # Add it to the output.
            postfix = postfix + c

    # Empty the operator stack and appends to top of stack.
    #Then removes it from the stack and returns the postfix
    while len(stack) != 0:
        postfix = postfix + stack[-1]
        stack = stack[:-1]

    return postfix

class State:
    """A state and its arrows in Thompson's construction."""
    def __init__(self, label, arrows, accept):
        """label is the arrow labels, arrows is a list of states to
           point to, accept is a boolean as to whether this is an accept
           state.
        """
        self.label = label
        self.arrows = arrows
        self.accept = accept
    
    def followes(self):
        """The set of states that are gotten from following this state
           and all its e arrows."""
        # Include this state in the returned set.
        states = {self}
        # If this state has e arrows, i.e. label is None.
        if self.label is None:
            # Loop through this state's arrows.
            for state in self.arrows:
                # Incorporate that state's earrow states in states.
                states = (states | state.followes())
        # Returns the set of states.    
        return states

class NFA:
    """A non-deterministic finite automaton."""
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def match(self, s):
        """Return True iff this NFA (instance) matches the string s."""
        # A list of previous states that we are still in.
        previous = self.start.followes()
        # Loop through the string, a character at a time.
        for c in s:
            # Start with an empty set of current states.
            current = set()
            # Loop throuth the previous states.
            for state in previous:
                # Check if there is a c arrow from state.
                if state.label == c:
                    # Add followes for next state.
                    current = (current | state.arrows[0].followes())
            # Replace previous with current.
            previous = current
        # If the final state is in previous, then return True. False otherwise. 
        return (self.end in previous)

def re_to_nfa(postfix):
    # A stack for NFAs.
    stack = []
    # Loop through the postfix r.e. left to right.
    for c in postfix:
        # Concatenation.
        if c == '.':
            # Pop top NFA off stack.
            nfa2 = stack[-1]
            stack = stack[:-1]
            # Pop the next NFA off stack.
            nfa1 = stack[-1]
            stack = stack[:-1]
            # Make accept state of NFA1 non-accept.
            nfa1.end.accept = False
            # Make it point at start state of nfa2.
            nfa1.end.arrows.append(nfa2.start)
            # Make a new NFA with nfa1's start state and nfa2's end state.
            nfa = NFA(nfa1.start, nfa2.end)
            # Push to the stack.
            stack.append(nfa)
        elif c == '|':
            # Pop top NFA off stack.
            nfa2 = stack[-1]
            stack = stack[:-1]
            # Pop the next NFA off stack.
            nfa1 = stack[-1]
            stack = stack[:-1]
            # Create new start and end states.
            start = State(None, [], False)
            end = State(None, [], True)
            # Make new start state point at old start states.
            start.arrows.append(nfa1.start)
            start.arrows.append(nfa2.start)
            # Make old end states non-accept.
            nfa1.end.accept = False
            nfa2.end.accept = False
            # Point old end states to new one.
            nfa1.end.arrows.append(end)
            nfa2.end.arrows.append(end)
            # Make a new NFA.
            nfa = NFA(start, end)
            # Push to the stack.
            stack.append(nfa)
        elif c == '*':
            # Pop one NFA off stack.
            nfa1 = stack[-1]
            stack = stack[:-1]
            # Create new start and end states.
            start = State(None, [], False)
            end = State(None, [], True)
            # Make new start state point at old start state.
            start.arrows.append(nfa1.start)
            # And at the new end state.
            start.arrows.append(end)
            # Make old end state non-accept.
            nfa1.end.accept = False
            # Make old end state point to new end state.
            nfa1.end.arrows.append(end)
            # Make old end state point to old start state.
            nfa1.end.arrows.append(nfa1.start)
            # Make a new NFA.
            nfa = NFA(start, end)
            # Push to the stack.
            stack.append(nfa)
        else:
            # Create an NFA for the non-special character c.
            # Create the end state.
            end = State(None, [], True)
            # Create the start state.
            start = State(c, [], False)
            # Point new start state at new end state.
            start.arrows.append(end)
            # Create the NFA with the start and end state.
            nfa = NFA(start, end)
            # Append the NFA to the NFA stack.
            stack.append(nfa)
    
    # There should only be one NFA on the stack.
    if len(stack) != 1:
        return None
    else:
        return stack[0]
    

        
def compare_re_to_file(fileName, isVerbose):
    #Declaring matches array to be displayed later
    infix = fileName[0]
    nI = len(fileName)
    
    for index in range(1, nI):
        textFile = fileName[index]
        print(textFile)
        
        matchesArray = []
        
    #Opens file from user input to be read
        with open(textFile, "r") as file:
        #Assigns contents of text file as a string
            for line in file:
            #Calls shunt function passing users input as argument, assigns it to postfix
                postfix = shunt(infix)
                nfa = re_to_nfa(postfix)
            #Divides the new String line into substrings and puts them in an array
                for expression in line.split():
                #Checks each substring for a match by calling match function in the nfa class
                    match = nfa.match(expression)
                #If there is a match, adds substring to matchesArray
                    if (match == True):
                        matchesArray.append(expression)

    #Displays both matches and amount if --verbose is used
        if isVerbose == True:
            print(len(matchesArray))
            print(matchesArray)
    #Displays both amount of matches by default
        elif isVerbose == False:
            print(len(matchesArray))
    

    
parser = argparse.ArgumentParser(description='Process file names')
#argument added for parsing expression and file name
parser.add_argument("file", nargs='+', help="select file to be used")
#argument added to display both matches and amount of matches
parser.add_argument("-v", "--verbose", action="store_true", help="display both matches and amount")
#assigning parsed args as variable
args = parser.parse_args()

#if --verbose passes True to confirm --verbose was used
if args.verbose:
    compare_re_to_file(args.file, True)
#by default pass False to only display amount of matches
else:
    compare_re_to_file(args.file, False)


    


     
     
        
