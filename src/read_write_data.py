"""Navigate file structure to read and write data appropriately.

Contains FileReader and FileWriter classes that both inherit from 
the FileNavigator class. These are used to organize the receipt
directories and files.

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

    def csv_locator(self, directory, recursive=True):

        if recursive:
            return self._csv_locator_recursive(directory)
        else:
            return self._csv_locator_single_dir(directory)
    
    def _csv_locator_recursive(self, directory):

        csv_filepaths = []
        for subdir, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.csv'):
                    csv_filepaths.append(os.path.join(subdir, filename))

        return csv_filepaths

    def _csv_locator_single_dir(self, directory):

        files = os.listdir(directory)
        csv_files = [f'{directory}/{file}' for file in files if file.endswith('.csv')]

        return csv_files

    def read_receipt(self, receipt_csv_path):

        return pd.read_csv(receipt_csv_path)
    


class FileWriter(FileNavigator):
    
    def __init__(self, receipts_dir):
        super().__init__(receipts_dir)

    def save_split_results(self, result_df, receipt_split_result_path):

        result_df.to_csv(receipt_split_result_path)

if __name__ == '__main__':

    receipts_dir = '/home/mike/finances/receipts'

    file_navigator = FileNavigator(receipts_dir)

    current_date = file_navigator._get_current_date()
    file_navigator._make_yr_mo_dir(current_date, suffix='_test')

    file_reader = FileReader(receipts_dir)

    csv_files = file_reader.csv_locator('/home/mike')