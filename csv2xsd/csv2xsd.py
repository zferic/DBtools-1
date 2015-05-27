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
import re

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


Format_String = \
"<xs:element name=\"_elename_\" nillable=\"true\">\n" + \
        "\t<xs:simpleType>\n" + \
          "\t\t<xs:restriction base=\"xs:string\">\n" + \
            "\t\t\t<xs:length value=\"200\" />\n" + \
          "\t\t</xs:restriction>\n" + \
        "\t</xs:simpleType>\n"    + \
      "</xs:element>\n"

Format_Date = \
"<xs:element name=\"_elename_\" type=\"xs:date\" nillable=\"true\">\n" + \
"</xs:element>\n"

Format_Time = \
"<xs:element name=\"_elename_\" type=\"xs:time\" nillable=\"true\">\n" + \
"</xs:element>\n"

Format_Int_Simple = \
"<xs:element name=\"_elename_\" type=\"xs:integer\" nillable=\"true\">\n" + \
"</xs:element>\n"

Format_Int_Range = \
"<xs:element name=\"_elename_\">\n" + \
   "\t<xs:simpleType>\n"    + \
      "\t\t<xs:restriction base=\"xs:integer\">\n"  + \
         "\t\t\t<xs:minInclusive value=\"_min_\"/>\n" + \
         "\t\t\t<xs:maxInclusive value=\"_max_\"/>\n" + \
      "\t\t</xs:restriction>\n"   + \
   "\t</xs:simpleType>\n" + \
"</xs:element>\n"

Format_Int_Enum_part1 = \
"<xs:element name=\"_elename_\" nillable=\"true\">\n" + \
    "\t<xs:simpleType>\n"   + \
        "\t\t<xs:restriction base=\"xs:integer\">\n"

                  
Format_Int_Enum_part3 = \
        "\t\t</xs:restriction>\n" + \
    "\t</xs:simpleType>\n"  + \
"</xs:element>\n"
  


# check data type
def GenTemplate(info):
    format_string = ""

    ## extract related fields
    field_name     = info[0]
    field_type     = info[3]
    field_choices  = info[5]
    field_note     = info[6]
    field_valid    = info[7]
    field_min      = info[8]
    field_max      = info[9]
    
    # change to lower case
    field_name = field_name.strip().lower()
    
    # remove the empty space    
    field_type = field_type.strip()


    
    if(field_type == 'notes'):
        # replace _elename_ in Format_String with the current field_name
        format_string = Format_String.replace('_elename_', field_name)


    
    if(field_type == 'text'):
            # check field_note whether contains the date info
            index_date = field_note.find('MM-DD-YYY')
            index_time = field_note.find('hh:mm') + field_note.find('Military Time')
            index_valid = field_valid.find('integer')
                  
            # Date
            if(index_date == -1):
                format_string = Format_Date.replace('_elename_', field_name)
            
            # Time
            if( index_time == -2 or index_time == -1):
                format_string = Format_Time.replace('_elename_', field_name)
            
            # Integers
            if(index_valid == -1):
                # integer list, check min and max
                field_min = field_min.strip()
                field_max = field_max.strip()
                if len(field_min) == 0 and len(field_max) == 0:
                    format_string = Format_Int_Simple.replace('_elename_', field_name)
                
                if len(field_min) > 0 and len(field_max) > 0:
                    format_string = Format_Int_Range.replace('_elename_', field_name)
                    format_string = format_string.replace('_min_', field_min)
                    format_string = format_string.replace('_max_', field_max)
                    
            # String
            if(index_date >= 0 and index_time >=0 and index_valid >= 0):
                 format_string = Format_String.replace('_elename_', field_name)
    
    
    
    if(field_type == 'radio' or field_type == 'checkbox'):
        # integer list
        list_int = []
        
        # extract integers out from field_choices
        sepintlist = field_choices.split('|')
        
        for item in sepintlist:
            # extract the 1st integer in each item
            found_int = re.search("\d+", item)
            list_int.append(found_int.group())
            
        #print list_int  
        format_str1 = Format_Int_Enum_part1.replace('_elename_', field_name)
        format_str3 = Format_Int_Enum_part3
        format_str2 = ""
        
        for i in list_int:
            format_str2 = format_str2 + "\t\t\t<xs:enumeration value=\"" + i + "\" />\n"
            
        format_string = format_str1 + format_str2 + format_str3

    return format_string
    
def main():
    
    # check the arguments
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    
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
    o_fname = filename + ".txt"
    o_file = open(o_fname, "w")

    # look at the second column, find the right table to work on
    for row in file:    
        tablename = row[1]
        tablename = tablename.strip()
        if tablename == "postpartum_data_abstraction":
            #print row[:2]
#            print row
        
            # the first column is the data field
            # to generate the xml format, we need to know
            # 1) data type  2) data range
            row_temp = GenTemplate(row)
            
            # output the row_temp to the text file
            o_file.write(row_temp)
#            print datatype


    # close output file
    o_file.close()
    
    return 0



if __name__ == '__main__':
    main()


