# Bill Splitter

An application to split an itemized receipt among multiple people.

This project was spawned by a trip to Costco with many items needed to be split evenly among a specific number of people and a few that were split unevenly.

The goal of the project was mostly to practice writing clean code, keeping a well organized project and writing some tests. It is still a work in progress.

Please let me know if you have any comments!!

## Current Master Branch Functionality

The program will search a given directory and all subdirectories that match the specific format "STORENAME_YYYY-MD-DD.csv". It will then create new files "STORENAME_YYYY-MD-DD_split.csv" for each file that matches the format.

These new files will be organized into directories named for each "YYYY-MM/" combination as determined by the file names.

Examples are in the "example/" directory.

No files will be deleted!

### Usage

First clone the repo to your local machine:

```bash
$ cd ~/some/path/to/keep/program/files
$ git clone https://github.com/MSDuncan82/bill-splitter
```

To run the program use:

```bash
$ cd ~/some/path/to/keep/program/files/bill-splitter.src
$ python main.py ~/path/to/receipts/dir
```
