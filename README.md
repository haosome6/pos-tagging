# POS Tagger
This is a part of speech tagger implemented Viterbi algorithm.  

## Description
For using it, training file(s) and test file need to be provided in txt format.

Example training file:
```
Adam : NP0
glared : VVD
back : AVP
at : PRP
him : PNP
and : CJC
looked : VVD-VVN
away : AV0
. : PUN
```

Example test file:
```
Of
course
he
is
.
```

The output file's name also need to be provided, and the format will looks like a training file.

## Usage
```bash
python3 tagger.py -d <training1.txt> <training2.txt> -t <test.txt> -o <output.txt>
```
