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





