"""Navigate file structure to read and write data appropriately.

The BillSplitter class can split an itemized bill between multiple people.
It can either split all items evenly or take in a list of purchase ids per
person. If given a list of purchase ids it will split each item's cost for 
only the people that bought it.

Typical usage example:

    splitter = BillSplitter(purchases_df)
    split_df = splitter.get_split_df()
    totals = splitter.get_totals() 
"""

import numpy as np
import pandas as pd
from datetime import datetime
import os

class FileNavigator(object):

    def __init__(self, receipts_dir):
        self.receipts_dir = receipts_dir
    
    def _make_yr_mo_dir(self, ts, suffix=None):

        try:
            date = datetime.date(ts)
        except TypeError:
            date = ts
        
        yr_mo_string = date.strftime('%Y-%m')
        directory_string = f'{yr_mo_string}{suffix}'
        
        try:
            os.mkdir(os.path.join(self.receipts_dir, directory_string))
        except FileExistsError:
            print('File already exists')

    def _get_current_date(self):

        return datetime.date(datetime.now())

class FileReader(FileNavigator):

    def __init__(self, receipts_dir):
        super().__init__(receipts_dir)

    def read_receipt(self, receipt_csv_path):

        return pd.read_csv(receipt_csv_path)

if __name__ == '__main__':

    file_navigator = FileNavigator('/home/mike/finances/receipts')

    current_date = file_navigator._get_current_date()
    file_navigator._make_yr_mo_dir(current_date, suffix='_test')