#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  File:        xxx.py
#  Author:      leiming <ylm@ece.neu.edu>
#  Copyright    2015
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

#-----------------------------------------------------------------------------#
#  Output:
#   unique_analyte          v1           v2             v3
#   A                      some_number  some_number some_number
#   B                      some_number  some_number some_number
#   C                      some_number  some_number some_number
#-----------------------------------------------------------------------------#

import pandas as pd
import numpy as np

filename = 'PROTECT combined phthalate data 5.11.15.csv'


def find_ind(analyte_list, analyte):
    # analyte_list is numpy.ndarray
    # analyte is str
    ind = 0
    for item in analyte_list:
        if item == analyte:
            break;
        ind = ind + 1

    return ind


def main():

    ## read analyte column, find the unique one
    df = pd.read_csv(filename)

    target_col =  df['analyte']
#    print type(target_col)

    ## remove the nan value
    target_col = target_col[pd.notnull(target_col)]
#    print target_col


    ## find the distinct value
    analyte_list = pd.unique(target_col)
    print analyte_list
#    print type(analyte_list)


    list_len = len(analyte_list)
#    print list_len

    odata = np.zeros((list_len, 3))

#    print odata
#    print type(odata)

    ## use odata[][] to index the element

    ## 1) read each row of input csv file (df)
    ## 2) look for analyte column, find the analyte type, calculate which row
    ##      to use
    ## 3) look for the visitid, find which visit (column) to increase the value
    ## 4) add 1 in odata[][] array
    ## 5) repeat from 1) to read next row till the end of file

#    print type(df)

    ## remove nan row in the dataframe
#    print df.shape[1]
    df = df.dropna(thresh=(df.shape[1]), axis=0)
#    print df


    ## index is the current row number, starting from 0
    ## row stores the current info
    for index, row in df.iterrows():
        visitid = row['visitid']
        visitid = int(visitid)

        analyte = row['analyte']

        colid = 0
        if visitid == 2:
            colid = 1

        if visitid == 3:
            colid = 2

        rowid = find_ind(analyte_list, analyte)

        odata[rowid][colid] = odata[rowid][colid] + 1
#        print index
#        print type(row['visitid'])
#        print type(row['analyte'])

#        if index == 5879:
#            print str(visitid) + ' ' + analyte

    ## save data to dataframe
    tab_list = ['v1', 'v2', 'v3']
    out_file = pd.DataFrame(odata, index=analyte_list, columns=tab_list)
    print out_file
    out_file.to_csv('pthalate_status.csv')

    return 0


if __name__ == '__main__':
    main()
