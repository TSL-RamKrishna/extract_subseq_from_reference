## Introduction

Extracts subsequence from reference sequence using mapping Start and End positions in Sam input file.

## Pre requisites

1) python3
2) biopython - Bio moudle

## Usage:

python extract_subseq_from_reference.py --reference reference.fasta --sam SAMFile 

### to extract 1000 bps from left and righ of the Start and End positions

python extract_subseq_from_reference.py --reference reference.fasa --sam SAMFile --left 1000 --right 1000
