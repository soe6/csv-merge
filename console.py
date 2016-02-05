#!/usr/bin/env python

from sys import argv
from time import time
from lib.csvmerge import merge_files
import lib.csvUtil
from os import getcwd, system


start_time = time()
cur_path = getcwd()
if len(argv) is not 6:
    print("CSV MERGER - Usage:")
    print("param 1: File to modify patch")
    print("param 2: Data file patch")
    print("param 3: index key from modify file")
    print("param 4: index key from data file")
    print("param 5: columns to append from data file, divided by \",\"")
    exit()

keyColumnMergeFile = argv[3]
keyColumnSourceFile = argv[4]
columns = str(argv[5]).split(",")
sourceFilePath = ''.join([cur_path, '/', argv[2]])
sourceFileData = lib.csvUtil.csv2dic(sourceFilePath, keyColumnSourceFile)
mergeFilePath = argv[1]

mod_rows_counter = merge_files(mergeFilePath, sourceFileData, keyColumnMergeFile, columns)
print("Finished in {0:.2f} seconds. Rows modified: {1:.0f}".format(time() - start_time, mod_rows_counter))
