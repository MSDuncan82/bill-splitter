import bill_splitter
import read_write_data
import sys
import pandas as pd

def get_csv_filepaths_with_meta(receipts_dirpath: str) -> list:
    
    file_reader = read_write_data.FileReader(receipts_dirpath)

    csv_filepaths = file_reader.find_csv_filepaths(receipts_dirpath)
    
    csv_filpaths_with_meta = []
    for csv_filepath in csv_filepaths:

        yr_mo_directory = file_reader.get_yr_mo_directory(csv_filepath)
        store_name = file_reader.get_store_name(csv_filepath)

        csv_meta_dict = {
            'csv_filepath':csv_filepath, 
            'yr_mo_directory':yr_mo_directory,
            'store_name':store_name 
            }

        csv_filpaths_with_meta.append(csv_meta_dict)

    return csv_filpaths_with_meta

def get_split_dfs_from_csv_files(csv_filpaths_with_meta: list) -> list:
    
    result_dfs_with_meta = csv_filpaths_with_meta.copy()

    for csv_filepath_with_meta_dict in result_dfs_with_meta:

        csv_filepath = csv_filepath_with_meta_dict['csv_filepath']
        purchases_df = pd.read_csv(csv_filepath)
        splitter = bill_splitter.BillSplitter(purchases_df)
        result_df = splitter.get_result_df()

        csv_filepath_with_meta_dict.update({'result_df':result_df})

    return result_dfs_with_meta

def save_split_dfs_to_csv(receipts_dirpath: str, result_dfs_with_meta: list):
    
    file_writer = read_write_data.FileWriter(receipts_dirpath)

    file_writer.save_split_results(result_dfs_with_meta)

def main(receipts_dirpath: str):

    csv_files_with_meta = get_csv_filepaths_with_meta(receipts_dirpath)
    result_dfs_with_meta = get_split_dfs_from_csv_files(csv_files_with_meta)
    save_split_dfs_to_csv(receipts_dirpath, result_dfs_with_meta)

if __name__ == '__main__':

    receipts_dirpath = sys.argv[1]
    main(receipts_dirpath)