#!/bin/sh

## combine all the csv files into one

FILES=*.csv
count=0
## parent folder name = target sample name
targetname=${PWD##*/} 

if [ -f $targetname.txt ]; then
	rm $targetname.txt
fi

touch $targetname.txt

savefilename=$targetname.csv

if [ -f $targetname.csv ]; then
	 savefilename=$targetname.csv_v1
fi



# read all the files in the current directory
for f in $FILES
do
	#
	if [ $count = 0 ]; then
		cat $f >> $targetname.txt
	else
		# remove the first row
		sed '1 d' $f >>  $targetname.txt
	fi

	count=$((count + 1))

done

mv $targetname.txt  $savefilename

