
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

if __name__ == "__main__":
    for infix in ["3+4*(2-1)", "1+2+3+4+5*6", "(1+2)*(4*(6-7))"]:
        print(f"infix:   {infix}")
        print(f"postfix: {shunt(infix)}")
        print()