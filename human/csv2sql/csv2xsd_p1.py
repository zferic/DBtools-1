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
# info[0]       :   field name
# info[1]       :   form name
# info[2]       :   section header
# info[3]       :   field type
# info[4]       :   field label
# info[5]       :   choices, calculations, labels
# info[6]       :   field note
# info[7]       :   Text Validation Type OR Show Slider Number
# info[8]       :   Text Validation Min
# info[9]       :   Text Validation Max
# info[10]      :   Identifier?
# info[11]      :   Branching Logic (Show field only if...)
# info[12]      :   Required Field?
# there are other fields, but not important

import sys
import csv
#import re

#modify the field types if necessary
FieldType = ['text','radio','notes', 'checkbox']

# for each field type, there could be multiple specific types
# For example,
#   text        :   date, char(string)
#   radio       :   integer list
#   checkbox    :   integer list
#   notes       :   char(string)

#   text->date  :   MM-DD-YYY / hh:mm / Military Time
#   text->char  :   char(200)
#   radio->integer list :   looking for '|' as separator and extract integers
#   checkbox->integer   :   same as radio
#   notes->char :   always char, using char(200) as default



Temp_mapping = \
"<edd:field source=\"small_name\" target=\"cap_name\"/>\n"



# the first column is the data field
# to generate the xml format, we need to know
# 1) data type  2) data range
def GenTemplate(info):
    format_string = ""

    ## extract related fields
    ## branching logic is not considered here
    field_name     = info[0]        # name
#    field_type     = info[3]        # data type
#    field_choices  = info[5]        # data options
#    field_note     = info[6]        # specific notes, such as date format
#    field_valid    = info[7]
#    field_min      = info[8]
#    field_max      = info[9]

    # change to lower case
    name_low = field_name.strip().lower()
    name_upp = field_name.strip().upper()

    # remove the empty space
    name_low = name_low.strip()
    name_upp = name_upp.strip()

    format_string = Temp_mapping.replace('small_name', name_low)
    format_string = format_string.replace('cap_name', name_upp)

    return format_string

def main():

    # check the arguments
    # print 'Number of arguments:', len(sys.argv), 'arguments.'
    print "program name : ", sys.argv[0]
    print "csv file : ", sys.argv[1]
    print "Start program."

    if len(sys.argv) == 1:
        print "Please specify the csv file."
        sys.exit()

    if len(sys.argv) > 2:
        print "Too many. Read one csv file at at time."
        sys.exit()

    filename = sys.argv[1]
    #print filename

    # read csv file
    file = csv.reader(open(filename, "rb"));

    # open text file to write
    o_fname = filename + "_part1.xsd"
    o_file = open(o_fname, "w")

    # look at the second column, find the right table to work on
    # You can specify which table to work on !!!
    for row in file:
        tablename = row[1]
        tablename = tablename.strip()
        if tablename == "postpartum_data_abstraction":

            row_temp = GenTemplate(row)

            # output the row_temp to the text file
            o_file.write(row_temp)

    # close output file
    o_file.close()

    #
    print "End program.\n",\
        "The decimal case is not considered here.\n",\
        "You still need to manually fix the output."

    return 0



if __name__ == '__main__':
    main()


