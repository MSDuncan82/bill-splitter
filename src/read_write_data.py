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
import re

class FileNavigator(object):

    def __init__(self, receipts_dirpath):
        self.receipts_dirpath = receipts_dirpath

    def get_yr_mo_directory(self, filepath):

        try:
            yr_str, mo_str, day_str = self._get_date_strings_from_file(filepath)
        except AttributeError:
            return -1
            
        yr_mo_directory = f'{yr_str}-{mo_str}'

        return yr_mo_directory

    def _get_date_strings_from_file(self, filepath):

        filename = filepath.split('/')[-1]
        pattern = r"_(.*?)\."
        
        date_str = re.search(pattern, filename).group(1)
        yr_str, mo_str, day_str = date_str.split('-')

        return yr_str, mo_str, day_str

    def make_yr_mo_dir_from_string(self, directory_string, suffix=''):
        
        if suffix: suffix = '_' + suffix

        directory_string = f'{directory_string}{suffix}'

        try:
            os.mkdir(os.path.join(self.receipts_dirpath, directory_string))
        except FileExistsError:
            pass
    
    def _get_yr_mo_string_from_timestamp(self, ts):

        try:
            date = datetime.date(ts)
        except TypeError:
            date = ts
        
        yr_mo_string = date.strftime('%Y-%m')

        return yr_mo_string

    def _get_current_date(self):

        return datetime.date(datetime.now())

class FileReader(FileNavigator):

    def __init__(self, receipts_dirpath):
        super().__init__(receipts_dirpath)

    def find_csv_files(self, directory, recursive=True):

        if recursive:
            return self._find_csv_files_recursive(directory)
        else:
            return self._find_csv_files_single_dir(directory)
    
    def _find_csv_files_recursive(self, dirpath):

        csv_filepaths = []
        for subdir, _, files in os.walk(dirpath):
            for filename in files:
                if filename.endswith('.csv'):
                    csv_filepaths.append(os.path.join(subdir, filename))

        return csv_filepaths

    def _find_csv_files_single_dir(self, dirpath):

        files = os.listdir(dirpath)
        csv_files = [f'{dirpath}/{file}' for file in files if file.endswith('.csv')]

        return csv_files

    def read_receipt(self, receipt_csv_path):

        return pd.read_csv(receipt_csv_path)
    
class FileWriter(FileNavigator):
    
    def __init__(self, receipts_dirpath):
        super().__init__(receipts_dirpath)

    def save_split_results(self, result_dfs_with_yr_mo_dir):

        for result_df, yr_mo_dir in result_dfs_with_yr_mo_dir:

            results_dirpath = os.path.join(self.receipts_dirpath, yr_mo_dir)
            results_filepath = os.path.join(results_dirpath, f'{yr_mo_dir}.csv')
            self.make_yr_mo_dir_from_string(results_dirpath)

            self._save_single_split_result_to_path(result_df, results_filepath)

    def _save_single_split_result_to_path(self, result_df, receipt_split_result_path):

        result_df.to_csv(receipt_split_result_path)

if __name__ == '__main__':

    receipts_dirpath = '/home/mike/projects/finance/bill-splitter/data'