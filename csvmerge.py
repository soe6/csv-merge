#!/usr/bin/env python

from sys import argv
import lib.csvUtil
from os import rename
from os import remove
from os import path
from os import getcwd
from csv import reader
from time import time

start_time = time()

if len(argv) is not 6:
    print("CSV MERGER - Usage:")
    print("param 1: File to modify patch")
    print("param 2: Data file patch")
    print("param 3: index key from modify file")
    print("param 4: index key from data file")
    print("param 5: columns to append from data file, divided by \",\"")
    exit()

curPath = getcwd()
keyColumnMergeFile = argv[3]
keyColumnSourceFile = argv[4]
columns = argv[5].split(",")
sourceFilePath = ''.join([curPath, '/', argv[2]])
sourceFile = lib.csvUtil.csv2dic(sourceFilePath, keyColumnSourceFile)
mergeFilePath = ''.join([curPath, '/', argv[1]])
bkFilePath = ''.join([mergeFilePath, "_bk"])

if not path.isfile(mergeFilePath):
    Exception("File not found!")
    exit()

if not path.isfile(bkFilePath):
    rename(mergeFilePath, bkFilePath)

keyColumnMergeFileId = -1
labels = []
mod_rows_counter = 0
with open(mergeFilePath, 'w') as out_file:
    with open(bkFilePath, 'r') as f:
        csv_reader = reader(f, delimiter=";")
        for k, items in enumerate(csv_reader):
            items = [x.decode('utf-8-sig') for x in items]
            if k is 0:
                keyColumnMergeFileId = items.index(keyColumnMergeFile)
                newLabels = items
                for col in columns:
                    newLabels.append(col.decode("utf-8-sig"))

                newLine = ';'.join(newLabels)
                out_file.writelines(''.join([newLine, '\n']).encode("utf-8"))
                labels = dict((k, v) for k, v in enumerate(items))
                continue

            itemMergeKey = items[keyColumnMergeFileId]
            if itemMergeKey in sourceFile:
                mod_rows_counter += 1
                for col in columns:
                    items.append(sourceFile[itemMergeKey][col.decode("utf-8-sig")])

            newLine = ';'.join(items)
            out_file.writelines(''.join([newLine, '\n']).encode("utf-8"))

remove(bkFilePath)
print("Finished in {0:.2f} seconds. Rows modified: {1:.0f}".format(time() - start_time, mod_rows_counter))
