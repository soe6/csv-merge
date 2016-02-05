# CSV MERGE #

### WINDOWS PACKAGE INSTALLER ###
https://github.com/soe6/csv-merge/releases

### DESCRIPTION ###
Csv Merge is a small application written in Python, with simple user interface writen in Kivy. 
It was created to save me some time while merging large csv data sets.
Basically it's an alternative to Excel's VLOOKUP function.
Processing large data sets can by really time consuming for VLOOKUP, this app does it fast.

Application is designed to work with UTF-8 encoded files. Other encoding formats probably won't work.

To make usage more efficient package installer adds "Append csv file..." option to Windows Explorer right-click menu.

### INSTALLATION ###
Windows - use the package installer

### USAGE ON WINDOWS (package installer) ###

1. Select csv file in Windows Explorer
2. On right-click menu select "Append csv file..."
3. Select second csv file (from with data will by appended)
4. Select key columns for main and second file (columns with same item names)
5. Select columns to be appended to main file
6. Hit execute

### Linux/Windows usage from console ###

Alternatively if you have Python (2.7) interpreter installed, 
you can run the app from console:
> cd /aplication_path

> python main.py

### Troubleshooting ###
If anything goes wrong, backup of the main csv is placed in the same file path with "_bk" suffix

### Licence ###
Csv Merge is licensed under the MIT License