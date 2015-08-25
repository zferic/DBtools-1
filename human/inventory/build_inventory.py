#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  csv2xsd.py
#  4/1/2015
#  Copyright 2015 leiming <ylm@ece.neu.edu>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


## Warnings: If the input structure changes, e.g. the redcap template, the
##          following code needs to be changed too. For more info, please
##          contact the author.

## current layout of the template
# info[0]       :   study_id


import sys
import csv
import os
#import re



def main():

    # check the arguments
    # print 'Number of arguments:', len(sys.argv), 'arguments.'
    print "program name : ", sys.argv[0]
    print "Start program."

    #-------------------------------------------------------------------------#
    #  (1) Find all the unique study ids
    #-------------------------------------------------------------------------#

    # intialize studyid
    studyid = []

    # list all the folders in current directory
    dirname = [name for name in os.listdir(".") if os.path.isdir(name)]
    columns = len(dirname) + 1

    for cur in dirname:
        # list all the csv files in the dir
        csvfiles = os.listdir(cur)
        for f in csvfiles:
            filelink = cur + "/" + f
            # read the csv files
            read_f = csv.reader(open(filelink, "rb"))

            # read study id of current file
            for row in read_f:
                studyid.append(row[0])

    # after reading all the studyid in all the files,
    # remove the strings in the list
    sid = [x for x in studyid if any(c.isdigit() for c in x)]

    # find the unique ids
    sid = set(sid)
    sid = sorted(sid)   # sort
    rows = len(sid) + 1
    #-------------------------------------------------------------------------#
    #   (2) Configure the output layout
    #       Iterate each file to label the id if it exists
    #-------------------------------------------------------------------------#
    print dirname
#    print columns, rows

    # Creates a list containing 5 lists initialized to 0
    table = [[0 for x in range(columns)] for x in range(rows)]

    print "rows : " + str(len(table))
    print "columns : " + str(len(table[0]))

    # fill the 1st row
    table[0][0] = "study_id"
    pos = 1
    for item in dirname:
        table[0][pos] = item
        pos = pos + 1

    # fill the 1st column
    pos = 1
    for id in sid:
        table[pos][0] = id
        pos = pos + 1

#    for i in table:
#        print i
#    print sid

    # go through each csv file
    target_column = 1
    for cur in dirname:
        # look at current column / directory
        csvfiles = os.listdir(cur)
        for f in csvfiles:
            filelink = cur + "/" + f
            # read the csv files
            read_f = csv.reader(open(filelink, "rb"))

            # read study id of current file
            for row in read_f:
                target = row[0]
                # check whether target exists in sid
                pos = 1
                for item in sid:
                    # if study id is there
                    # label and break, go to next id in the csv file
                    if (target == item):
                        table[pos][target_column] = 1
                        break
                    pos = pos + 1

        # check the next column / directory
        target_column = target_column + 1

#    for i in table:
#        print i

    #-------------------------------------------------------------------------#
    #   (3) Output table to csv
    #-------------------------------------------------------------------------#

    # open text file to write
    o_fname = "humansubject_inventory_list.csv"


    writer = csv.writer(open(o_fname, 'w'))
    for row in table:
        writer.writerow(row)
#    with open(o_fname, 'wb') as f:
#        writer = csv.writer(f)
#        for row in table:
#            print row
#            writer.writerows(row)
#    o_file = open(o_fname, "w")
#
#    for row in table:
##        print row
#        datastr = ''
#        for item in row:
#            datastr = datastr + str(item) + ","
#
#        # remove the last comma
##        datastr = datastr.replace(datastr[len(datastr) - 1], '\n')
##        print datastr
#        o_file.write(datastr)
#
#    # close output file
#    o_file.close()


    print "End program."

    return 0



if __name__ == '__main__':
    main()


