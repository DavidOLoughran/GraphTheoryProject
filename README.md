# Compare Regular Expressions to Text File(s)
This is a Python 3 script that takes a regular expression and a file(s) as command line argumenta and outputs the number of matches within the text file(s).<br/>

- The repository contains a Python3 script called `rescript.py` and two text files `input.txt` and `test.txt`

## Getting Started
- [Install](https://www.python.org/downloads/) Python 3<br/>
```sh
   $ sudo apt-get install python3.6
   ```
- Download / Clone this repository into a folder through the command line.<br/>
 ```sh
   $ git clone -b master https://github.com/DavidOLoughran/GraphTheoryProject.git
   ```


## How To Run
Navigate the command line until you are inside the projects folder.<br/>

Once in the correct folder type the following command in the command line:
```sh
   $ python3 rescript.py f.a.b input.txt test.txt
   ```
- This will display the name of the file and its number of matches below in order. ie:
```
   input.txt
   1
   ```

- To see a list of all availabe options and how to use the program use the following command:
```sh
   $ python3 rescript.py -h
   ```
- The following command can be used to also display a list of the matches found:
```sh
   $ python3 rescript.py a.b input.txt test.txt --verbose
   ```
   
**NOTE:** The regular expression has to be before the file names or the program will crash

## How It Works
### Shunting Yard Algorithm
First we pass the infix notation from the command line into the Shunting Yard Alorithm defined as shunt(infix).

- We then define the order of precedence for the following operators ( . , *, | ).
- We loop through the infix and while theres an operator with greater precedence we pop it off the stack and put it into the output queue. 
- Push the current operator onto the stack.
- If the operator is a left bracket it gets pushes onto the stack. 
- However if its a right bracket we loop through the stack while its not a left bracket at the top of a stack the operators are popped from the stack and into the output queue.
- The left bracket gets popped of the stack and is discarded
- If it is a literal character/number, it gets added to the output queue
- Empty the operator stack and append it to the top, remove it from the stack and returns the postfix
```sh
   for c in infix:
        if c in {'*', '.', '|'}:
            while len(stack) > 0 and stack[-1] != '(' and prec[stack[-1]] >= prec[c]:
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            stack = stack + c
        elif c == '(':
            stack = stack + c
        elif c == ')':
            while stack[-1] != "(":
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            stack = stack[:-1]             
        else:
            postfix = postfix + c

    while len(stack) != 0:
        postfix = postfix + stack[-1]
        stack = stack[:-1]

    return postfix
   ```
### Thompsons Contruction
#### Regular Expression to Nondeterministic Finite Automaton

- First a State class is initialised with a self state, label, arrows and an accept state. Label is the arrow labels, arrows is a list of states topoint to, accept is a boolean as to whether this is an accept state.

- Second an NFA class gets initialised with a self state, start state and end state to later be used check for matches in a match function.<br/>

A function was then created to take the postfix expression created by the Shunting Yard Algorithm and converts it to a Nondeterministic Finite Automaton. <br/>
First a stack is initialised and then we loop through the postfix expression from left to right.<br/>

##### Below are the steps taken if the character is a Concatenation ( . )  <br/>

- First you pop the top NFA of the stack (NFA2) followed by the next NFA of the stack(NFA1). The first going on the right and next on the left of the stack.
- You then take accept state from NFA1 and make it no longer an accept state.
- Then you make it point at the start state of NFA2 to create a path from nfa1 to nfa2.
- Create a new NFA with NFA1's start state and NFA2's end state.
- Finally push it to the stack
```sh
   if c == '.':
            nfa2 = stack[-1]
            stack = stack[:-1]

            nfa1 = stack[-1]
            stack = stack[:-1]

            nfa1.end.accept = False

            nfa1.end.arrows.append(nfa2.start)

            nfa = NFA(nfa1.start, nfa2.end)

            stack.append(nfa)
   ```
   
##### Below are the steps taken if the character is an OR Operator ( | )  <br/>

- First you pop the top NFA of the stack (NFA2) followed by the next NFA of the stack(NFA1). The first going on the right and next on the left of the stack.
- You then create new start and end states and make them point at the old start states.
- Then make the old end states (NFA1 and NFA2) non-accept states and point them to new states .
- Create a new NFA.
- Finally push it to the stack

```sh
   elif c == '|':
            nfa2 = stack[-1]
            stack = stack[:-1]

            nfa1 = stack[-1]
            stack = stack[:-1]

            start = State(None, [], False)
            end = State(None, [], True)

            start.arrows.append(nfa1.start)
            start.arrows.append(nfa2.start)

            nfa1.end.accept = False
            nfa2.end.accept = False

            nfa1.end.arrows.append(end)
            nfa2.end.arrows.append(end)

            nfa = NFA(start, end)

            stack.append(nfa)
   ```
##### Below are the steps taken if the character is a Kleene's Star ( * )  <br/>

- First you pop one NFA of the stack(NFA1).
- You then create new start and end states and make them point at the old start states.
- Then make the start state point at the old start state and at the new end state.
- Make the old end state non accept and point it to a new end and start state.
- Create a new NFA.
- Finally push it to the stack

```sh
   elif c == '*':
            nfa1 = stack[-1]
            stack = stack[:-1]

            start = State(None, [], False)
            end = State(None, [], True)

            start.arrows.append(nfa1.start)

            start.arrows.append(end)

            nfa1.end.accept = False

            nfa1.end.arrows.append(end)

            nfa1.end.arrows.append(nfa1.start)

            nfa = NFA(start, end)
            stack.append(nfa)
   ```
   
##### Below are the steps taken if it is a non-special character (literal character) <br/>

- First you have to create the end state and the start state
- Point the new start state at the new end state .
- Create a new NFA with the start and end states.
- Finally push it to the stack

```sh
   else:
            end = State(None, [], True)

            start = State(c, [], False)

            start.arrows.append(end)

            nfa = NFA(start, end)

            stack.append(nfa)
   ```
**NOTE:** There should only be one NFA on the Stack
- After checking to make there is only one NFA on the stack, The stack can be returned to the function.





