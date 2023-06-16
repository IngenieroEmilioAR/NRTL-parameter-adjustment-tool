# NRTL-parameter-adjustment-tool

The NRTL parameter adjustment tool is a program in which the user can estimate binary interaction parameters of a mixture of two components, using user-provided experimental data.

# How to use

Download the whole code. Make sure you have all libraries and packages listed in "Requiremets.txt" or set up your virtual environment with it. 

Once you have it, just run Main.py file and follow the instructions in the status chart at bottom left.

## Experimental data

The tool offers flexibility by introducing your own experimental data. Required information is listed below:
- Vapor and liquid composition for a particular component at different temperatures in Kelvin. 
- It is also needed (for both components) the coefficients for the Antoine equation in the form log10(P) = A - B/(T-C), where P is in mmHg and T in °C.

> Please, check in example experimental data the files "example simple data"

The datafiles you will use have these conditions:

- Either .xlsx or .csv format can be used.
- Data needs to have specific headers (example is below).
- Avoid reporting data for zero composition either from liquid or vapor phase.


### Example of experimental data for acetone - chloroform system

|T (K)| x1 | y1 | Acetone (1) | Chloroform (2) |
|---|---|---|---|---|
|335.75|	0.098 |	0.06 |	7.31742 |	7.11289 |
| 336.65 |	0.186 |	0.143 |	1315.6735 |	1233.0732 |
|337.25 |	0.266 |	0.23 |	240.479 |	230.213 |
|337.55 |	0.36 |	0.36	| | |
|...|...|...|...|...|
|330.15 |	0.949 |	0.975	|  |	|
