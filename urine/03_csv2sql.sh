#!/bin/bash
echo -ne "Author: Leiming Yu (ylm@ece.neu.edu)
\tNortheastern University

Usage:\t ./sql.sh xxx.csv\n\n
"

#check the number of arguments
if [ $# -ne 1 ]
then
	echo "$0 : you must provide the csv file"
	exit 1
fi


#input file name
FILE=$1

#format output file name
OFILE=`echo $FILE | cut -d'.' -f1 | awk '{print "dt_"$1".sql"}'`
echo $OFILE
DTNAME=`echo $FILE | cut -d'.' -f1 | awk '{print "dt_"$1}'`
echo $DTNAME

# extract each field
awk -F ',' '{print $2}' $FILE | sed -e '/^$/d' -e '1d' > out

# uppercase
sed -i 's/./\U&/g' out

# append template line 
awk '{print $1}' out | awk '{print $1"\n""CONSTRAINT CK_"$1" CHECK( ),"}' > $OFILE 

# add header
sed -i '1i USE PROTECT_E\n\nGO\n\nCREATE TABLE '"$DTNAME"'(' $OFILE

# add tailer
cat tailer >> $OFILE

echo "check the output file : "$OFILE

rm out
