"""Navigate file structure to read and write data appropriately.

Contains FileReader and FileWriter classes that both inherit from 
the FileNavigator class. These are used to organize the receipt
directories and files.

Typical usage example:

    file_reader = read_write_data.FileReader(receipts_dirpath)
    file_writer = read_write_data.FileWriter(receipts_dirpath)

    csv_filepaths = file_reader.find_csv_filepaths(receipts_dirpath)
    file_writer.save_split_results(result_dfs_with_meta)
"""

import numpy as np
import pandas as pd
from datetime import datetime
import os
import re

class FileNavigator(object):

    def __init__(self, receipts_dirpath):
        self.receipts_dirpath = receipts_dirpath

    def get_store_name(self, filepath):

        filename = filepath.split('/')[-1]
        store_name = filename.split('_')[0]
        
        return store_name

    def get_yr_mo_directory(self, filepath):

        yr_str, mo_str, day_str = self._get_date_strings_from_filepath(filepath)
        yr_mo_directory = f'{yr_str}-{mo_str}'

        return yr_mo_directory

    def make_yr_mo_dir_from_string(self, directory_string, suffix=''):
        
        if suffix: suffix = '_' + suffix

        directory_string = f'{directory_string}{suffix}'

        try:
            os.mkdir(os.path.join(self.receipts_dirpath, directory_string))
        except FileExistsError:
            pass

    def _get_date_strings_from_filepath(self, filepath):

        filename = filepath.split('/')[-1]
        pattern = r"_(.*?)\."
        
        date_str = re.search(pattern, filename).group(1)
        yr_str, mo_str, day_str = date_str.split('-')

        return yr_str, mo_str, day_str
    
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

    def get_csv_filepaths_with_meta(self):
        
        csv_filepaths = self._find_csv_filepaths(self.receipts_dirpath)
        
        csv_filpaths_with_meta = []
        for csv_filepath in csv_filepaths:

            yr_mo_directory = self.get_yr_mo_directory(csv_filepath)
            store_name = self.get_store_name(csv_filepath)

            csv_meta_dict = {
                'csv_filepath':csv_filepath, 
                'yr_mo_directory':yr_mo_directory,
                'store_name':store_name 
                }

            csv_filpaths_with_meta.append(csv_meta_dict)

        return csv_filpaths_with_meta

    def read_receipt(self, receipt_csv_path):

        return pd.read_csv(receipt_csv_path)

    def _find_csv_filepaths(self, dirpath, recursive=True):

        if recursive:
            return self._find_csv_files_recursive(dirpath)
        else:
            return self._find_csv_files_single_dir(dirpath)
    
    def _find_csv_files_recursive(self, dirpath):

        csv_filepaths = []
        for subdir, _, files in os.walk(dirpath):
            for filename in files:
                if self._filename_matches_receipt_format(filename):
                    csv_filepaths.append(os.path.join(subdir, filename))

        return csv_filepaths

    def _find_csv_files_single_dir(self, dirpath):

        files = os.listdir(dirpath)
        csv_files = [
            f'{dirpath}/{filename}' for filename in files 
            if self._filename_matches_receipt_format(filename)
            ]

        return csv_files

    def _filename_matches_receipt_format(self, filename):

        pattern = r'^[A-Z]+_[\d]{4}-[\d]{2}-[\d]{2}.csv$'

        return re.match(pattern, filename)
    
class FileWriter(FileNavigator):
    
    def __init__(self, receipts_dirpath):
        super().__init__(receipts_dirpath)

    def save_split_results(self, result_dfs_with_meta):

        for result_df_with_meta_dict in result_dfs_with_meta:
            
            result_df = result_df_with_meta_dict['result_df']
            yr_mo_string = result_df_with_meta_dict['yr_mo_directory']
            store_name = result_df_with_meta_dict['store_name']

            results_dirpath = os.path.join(
                self.receipts_dirpath, yr_mo_string
                )
            results_filepath = os.path.join(
                results_dirpath, f'{store_name}_{yr_mo_string}_split.csv'
                )
            self.make_yr_mo_dir_from_string(results_dirpath)

            self._save_single_split_result_to_path(result_df, results_filepath)

    def _save_single_split_result_to_path(self, result_df, 
                                          receipt_split_result_path):

        result_df.to_csv(receipt_split_result_path)

if __name__ == '__main__':

    receipts_dirpath = '/home/mike/projects/finance/bill-splitter/data'