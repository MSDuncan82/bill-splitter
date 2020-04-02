import bill_splitter
import read_write_data
import sys
import pandas as pd

def get_csv_files_with_yr_mo_dir_list(receipts_dirpath: str) -> list:
    
    file_reader = read_write_data.FileReader(receipts_dirpath)
    csv_files = file_reader.find_csv_files(receipts_dirpath)

    yr_mo_dirs = [
        file_reader.get_yr_mo_directory(csv_file) for csv_file in csv_files
        ]
    
    csv_files_with_yr_mo_dir = [
        (csv_file, yr_mo_dirs) for csv_file, yr_mo_dirs in zip(csv_files, yr_mo_dirs) if yr_mo_dirs != -1
        ]

    return csv_files_with_yr_mo_dir

def get_split_dfs_from_csv_files(csv_files_with_yr_mo_dir: list) -> list:
    
    result_dfs_with_yr_mo_dir = []
    for csv_file, yr_mo_dir in csv_files_with_yr_mo_dir:

        purchases_df = pd.read_csv(csv_file)
        splitter = bill_splitter.BillSplitter(purchases_df)
        result_df = splitter.get_result_df()

        result_dfs_with_yr_mo_dir.append((result_df, yr_mo_dir))

    return result_dfs_with_yr_mo_dir

def save_split_dfs_to_csv(receipts_dirpath, result_dfs_with_yr_mo_dir):
    
    file_writer = read_write_data.FileWriter(receipts_dirpath)

    file_writer.save_split_results(result_dfs_with_yr_mo_dir)

def main(receipts_dirpath):

    csv_files_with_yr_mo_dir = get_csv_files_with_yr_mo_dir_list(receipts_dirpath)
    result_dfs_with_yr_mo_dir = get_split_dfs_from_csv_files(csv_files_with_yr_mo_dir)
    save_split_dfs_to_csv(receipts_dirpath, result_dfs_with_yr_mo_dir)

if __name__ == '__main__':

    receipts_dirpath = sys.argv[1]

    main(receipts_dirpath)