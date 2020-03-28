# Constraint-Based Automated Updating of Application Deployment Models

This repository contains the prototype for the bachelor thesis    
"Constraint-Based Automated Updating of Application Deployment Models"   
The motivating scenario in the [thesis](thesis.pdf) is included in the edmm/ folder and will be run by default.  

## Overview

![Overview](images/overview.png "Overview")

The approach converts an [Essential Deployment Meta Model](https://github.com/UST-EDMM/spec-yaml) to a PDDL problem which is then solved by a planner. The domain ensures that the model is deploy able and the goal state tells the planner which components to update. Many deployment models can be converted to EDMM by using a [converter](https://github.com/UST-EDMM/transformation-framework). However, this prototype can easily be changed to import different deployment models in the future.

## Setup
This project uses a planner to update deployment models. As of right now, 
[Fast Downward](http://www.fast-downward.org/) and [Marvin](https://nms.kcl.ac.uk/planning/software/marvin.html) are supported. The path to the executables has to be specified in the [config.ini](config.ini) file.   
The prototype can not be run without a planner!

## Requirements
can be found in [requirements.txt](requirements.txt)

```
pip3 install -r requirement.txt
```
installes all necessary requirements for python3

```
python3 main.py
```
runs the prototype

## Analyzer
The script ``` analyzer/commandline_wrapper.py ``` is able to analyze outputs of the following planners: [Jasper](https://www.semanticscholar.org/paper/Jasper-%3A-the-Art-of-Exploration-in-Greedy-Best-Xie-M%C3%BCller/70b994eee371224a4530b602118cfc556c309f4b) and [Fast Downward](http://www.fast-downward.org/). Support for Marvin might be added in the future.  

### Usage
The analyzer can be used by piping the output to the script.   
Example: ``` cat output_file | python3 commandline_wrapper.py ```      
Multiple outputs of different planners can be merged in a single file. But above each output a line has to be added which tells the analyzer what kind of planner has produced the output.   
Example for a single Fast Downward output file:      
```
<<<<FD>>>>
INFO     Running translator.
INFO     translator stdin: None
...
```
Example for a single Jasper output file:      
```
<<<<JASPER>>>>
1. Running translator
Parsing... [0.000s CPU, 0.003s wall-clock]
...
```