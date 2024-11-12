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
