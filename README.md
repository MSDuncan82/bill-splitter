# Bill Splitter

An application to split an itemized receipt among multiple people.

This project was spawned by a trip to Costco with many items needed to be split evenly among a specific number of people and a few that were split unevenly.

The goal of the project was mostly to practice writing clean code, keeping a well organized project and writing some tests. It is still a work in progress.

Please let me know if you have any comments!!

## Current Master Branch Functionality

The program will search a given directory and all subdirectories that match the specific format *STORENAME_YYYY-MM-DD.csv*. It will then create new files *STORENAME_YYYY-MM-DD_split.csv* for each file that matches the format.

These new files will be organized into directories named for each "YYYY-MM/" combination as determined by the file names.

The template.csv for a receipt is in the */example* directory.

No files will be deleted!

### Usage

I have `splitbills` in my ~/bin folder which is on my path. This allows me to use the command `$ splitbills` from anywhere on my machine to run the script. Much of the code for execution is hardcoded so it may take some edits to make it work on your machine. A more user friendly version is a work in progress.
