#!/bin/sh

## convert dat file, extracted from t2d file (marker view) to csv file

FILES=*.dat

# read all the files in the current directory
for f in $FILES
do
	# deliminate by dot
	NAME=`echo $f | cut -d "." -f1`

	# add suffix
	csvfile=${NAME}.csv

	# remove blank line and white space
	sed '/^ *$/d' $f > tmp1.txt

	# lines of tmp1
	linenum=`wc -l < tmp1.txt`
	half=`expr $linenum / 2`

	## sperate it into 2 files
	head -n $half tmp1.txt > a.txt
	tail -n $half tmp1.txt > b.txt

	## parent folder name = target sample name
	targetname=${PWD##*/} 
	sed -e 's/[0-9]*\.[0-9]*/'$targetname'/g'  a.txt > targetname.txt 
	#echo $NAME

	## NAME is the file id
	sed -e 's/[0-9]*\.[0-9]*/'$NAME'/g'  a.txt > name.txt 

	#
	paste targetname.txt name.txt a.txt b.txt > ab.txt 
	sed '1,2 d' ab.txt > ab_tmp.txt
	sed -i '1s/^/target\tms_id\tmass_intensity\tpeaks\n/' ab_tmp.txt 
	cat ab_tmp.txt | tr "\\t" "," > $csvfile 

done

rm -rf tmp1.txt a.txt b.txt ab.txt ab_tmp.txt targetname.txt name.txt
