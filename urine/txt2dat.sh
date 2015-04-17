#!/bin/sh

## t2d files are extracted to txt file
## this bash script extract the m/z and intensity
## from the text files where data are on line 65 and 68

FILES=*.txt
for f in $FILES
do
	# deliminate by dot
	NAME=`echo $f | cut -d "." -f1`

	# add suffix
	o_file=${NAME}.dat

	# extract data from each text
	# output them to dat file 
	# using awk and sed
	awk '(NR==65) || (NR==68)' $f | sed "s/ \+/\n/g" > $o_file 
done
