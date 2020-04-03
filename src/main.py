from src.split_costs import SplitBill
from src.read_write_data import FileReader
from src.read_write_data import FileWriter
import sys
import pandas as pd

def get_csv_filepaths_with_meta(receipts_dirpath: str) -> list:
    
    file_reader = FileReader(receipts_dirpath)

    csv_filpaths_with_meta = file_reader.get_csv_filepaths_with_meta()

    return csv_filpaths_with_meta

def get_split_costs(csv_filpaths_with_meta: list) -> list:
    
    return [
        SplitBill(**csv_filpath_with_meta) for csv_filpath_with_meta in csv_filpaths_with_meta
        ]

    # for csv_filepath_with_meta_dict in result_dfs_with_meta:

    #     csv_filepath = csv_filepath_with_meta_dict['csv_filepath']
    #     purchases_df = pd.read_csv(csv_filepath)
    #     splitter = BillSplitter(purchases_df)
    #     result_df = splitter.get_result_df()

    #     csv_filepath_with_meta_dict.update({'result_df':result_df})

    # return result_dfs_with_meta

def save_split_dfs_to_csv(receipts_dirpath: str, split_costs_list: list):
    
    file_writer = FileWriter(receipts_dirpath)

    file_writer.save_split_results(split_costs_list)

def main(receipts_dirpath: str):

    csv_files_with_meta = get_csv_filepaths_with_meta(receipts_dirpath)
    split_costs_list = get_split_costs(csv_files_with_meta)
    save_split_dfs_to_csv(receipts_dirpath, split_costs_list)

if __name__ == '__main__':

    receipts_dirpath = sys.argv[1]
    main(receipts_dirpath)