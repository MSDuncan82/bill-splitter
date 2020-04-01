import bill_splitter
import read_write_data
import sys

def get_csv_files(receipts_dir):
    pass

def split_receipt_csv_files(csv_files):
    pass

def save_split_dfs_to_csv(split_dfs):
    pass

def main(receipts_dir):

    csv_files = get_csv_files(receipts_dir)

    split_receipt_dfs = split_receipt_csv_files(csv_files)

    save_split_dfs_to_csv(split_receipt_dfs)

if __name__ == '__main__':

    receipts_dir = sys.argv[0]

    main(receipts_dir)