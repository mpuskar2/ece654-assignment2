# This repository contains three files of importance:

## cfgAnalyzer.py
* This file contains the class used to analyze the parity of variables using a CFG.
* There is a sample block of code in the file, when the file is run the code is analyzed and the results are printed

## test.py
* This file defines the test cases using the unittest module

## ci.yml
* This file defines the CI workflow for when code is pushed to the repository
* The test file is run with python 3.10 as this is the version I have installed locally
* Installs pip dependencies and required apt libraries

## Sample output
* For the code:
```
x = 2
y = 3
z = x + y
if z % 2 == 0:
    z = z * 2
else:
    z = z * 3
```
* We get output:
```
Node 0: start
Variable x: U
Variable y: U
Variable z: U
Node 1: x = 2
Variable x: E
Variable y: U
Variable z: U
Node 2: y = 3
Variable x: E
Variable y: O
Variable z: U
Node 3: z = (x + y)
Variable x: E
Variable y: O
Variable z: O
Node 4: if: ((z % 2) == 0)
Variable x: E
Variable y: O
Variable z: O
Node 5: z = (z * 2)
Variable in branch x: E
Variable in branch y: O
Variable in branch z: E
Node 6: z = (z * 3)
Variable in branch x: E
Variable in branch y: O
Variable in branch z: O
Node 7: stop
Variable x: E
Variable y: O
Variable z: B
```
