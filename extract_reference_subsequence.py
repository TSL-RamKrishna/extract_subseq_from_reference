#!/usr/bin/env python3
## python program to extract subsequnces from reference using positions of mapped sequences in sam/bam file

import os, sys
import argparse
from Bio import SeqIO

parser=argparse.ArgumentParser(description="extract reference subsequnces using mapped positions", version="0.1")
parser.add_argument("--reference", dest="reference", action="store", help="reference sequenced used in mapping the reads")
parser.add_argument("--sam", dest="sam", action="store", help="sam file format of mapped reads")
parser.add_argument("--output", dest="output", action="store", default="extracts.fasta", help="Output file name")

options=parser.parse_args()


if not options.reference or not options.sam:
	print("You have not given either a reference sequence or a SAM file in your input. Please provide the input file. See help using --help option")
	exit(1)
if not os.path.exists(options.reference):
	print("Path to the reference input does not exists")
	exit(1)
elif not os.path.exists(options.sam):
	print("Path to the SAM input does not exists")
	exit(1)
else:
	pass


## read SAM file format and store mapStart and mapEnd in a dict structure
mappingData={}
with open(options.sam) as fsam:
	for line in fsam:
		line=line.rstrip()
		if line=="": continue
		if line.startswith("@"): continue
		linearray=line.split()
		mapID=linearray[0]
		mapChr=linearray[2]
		mapStart=int(linearray[3])
		mapString=linearray[9]
		mapEnd=mapStart + len(mapString) - 1
		if mapChr in mappingData.keys():
			mappingData[mapChr]["Start"].append(mapStart)
			mappingData[mapChr]["End"].append(mapEnd)
			mappingData[mapChr]["IDs"].append(mapID)
		else:
			mappingData[mapChr]={"Start":[mapStart], "End":[mapEnd], "IDs":[mapID]}




## Now read the reference sequence
referenceData={}
with open(options.reference) as freference:
	for record in SeqIO.parse(freference, "fasta"):
		seqid=record.id
		ntseq=str(record.seq)
		referenceData[seqid] = ntseq


#print(mappingData)
#print(referenceData)

def extract_subseq_from_reference(sequence, Start, End, left=1000, right=1000):
	return sequence[Start-left:End+right]


for chromosome in referenceData.keys():
	# lets get subsequence by chromosome
	if chromosome in mappingData.keys():
		for seqid, Start, End in zip(mappingData[chromosome]["IDs"], mappingData[chromosome]["Start"], mappingData[chromosome]["End"]):
			print(">" + seqid + "\n" + extract_subseq_from_reference(referenceData[chromosome], Start, End, 2, 2) )  # the first 1000 is the number of bases we want to the left of Start and second is the number of bases in right of End position we wnat to extract

exit(0)
