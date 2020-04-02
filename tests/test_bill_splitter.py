import pytest
import numpy as np
import pandas as pd
import sys
import os
os.chdir("..")
sys.path.append(os.getcwd())
from src.bill_splitter import BillSplitter
from src.read_write_data import FileReader

file_reader = FileReader('tests/data/')
csv_filepaths_with_meta = file_reader.get_csv_filepaths_with_meta()
csv_filepath = csv_filepaths_with_meta[1]['csv_filepath']
purchases_df = pd.read_csv(csv_filepath)
splitter = BillSplitter(purchases_df)

class TestBillSplitter(object):

    def test_init(self):
        pd.testing.assert_frame_equal(splitter.purchases_df, purchases_df)

    def test_get_result_df(self):
        true_result_df = pd.read_csv('tests/data/true_result.csv', index_col=0)
        true_result_df.index = true_result_df.index.astype(str)
        splitter_result_df = splitter.get_result_df()

        pd.testing.assert_frame_equal(
            splitter_result_df, 
            true_result_df
            )  

    def test_get_totals(self):
        true_totals_ser = pd.read_csv(
            'tests/data/true_result.csv', 
            skiprows=[1,2,3,4], 
            index_col=0
            ).iloc[0, 1:]
        splitter_totals_ser = splitter.get_totals()

        pd.testing.assert_series_equal(
            splitter_totals_ser,
            true_totals_ser
            )

    def test_get_split_df(self):
        true_split_df = pd.DataFrame.from_dict(
            {'product': 
                {0: 'MG cracker',
                1: 'Odell Beer',
                2: 'Med Salad Kit',
                3: 'Spring Mix'},
            'price': {0: 1.00, 1: 40.00, 2: 2.00, 3: 2.00},
            'andrew': {0: 1.00, 1: 0.00, 2: 0.00, 3: 0.00},
            'mike': {0: 0.00, 1: 30.00, 2: 0.00, 3: 1.00},
            'savannah': {0: 0.00, 1: 10.00, 2: 0.00, 3: 1.00},
            'scott': {0: 0.00, 1: 0.00, 2: 2.00, 3: 0.00}}
            )
        splitter_split_df = splitter.get_split_df()

        pd.testing.assert_frame_equal(
            splitter_split_df, 
            true_split_df
            )

    def test_get_products_df(self):
        true_products_df = pd.read_csv(
            'tests/data/true_result.csv', 
            usecols=['product', 'price'],
            nrows=4)
        splitter_products_df = splitter._get_products_df(purchases_df)

        pd.testing.assert_frame_equal(
            splitter_products_df, 
            true_products_df
            )

    def test_get_buyers_split_df(self):
        true_buyers_split_df = pd.DataFrame(
            {'andrew': {0: 1.0, 1: 0.0, 2: 0.0, 3: 0.0},
            'mike': {0: 0.0, 1: 30.0, 2: 0.0, 3: 1.0},
            'savannah': {0: 0.0, 1: 10.0, 2: 0.0, 3: 1.0},
            'scott': {0: 0.0, 1: 0.0, 2: 2.0, 3: 0.0}}
            )
        splitter_buyers_split_df = splitter._get_buyers_split_df(purchases_df)

        pd.testing.assert_frame_equal(
            splitter_buyers_split_df, 
            true_buyers_split_df
            )
    
    def test_get_buyers_split_perc_df(self):
        true_buyers_split_perc_df = pd.DataFrame(
            {'andrew': {0: 1.0, 1: 0.0, 2: 0.0, 3: 0.0},
            'mike': {0: 0.0, 1: 0.75, 2: 0.0, 3: 0.5},
            'savannah': {0: 0.0, 1: 0.25, 2: 0.0, 3: 0.5},
            'scott': {0: 0.0, 1: 0.0, 2: 1.0, 3: 0.0}}
        )

        buyers_only_df = (
            purchases_df.drop(['product', 'price'], axis=1).fillna(0)
            )
        splitter_buyers_split_perc_df = (
            splitter._get_buyers_split_perc_df(buyers_only_df)
            )
        
        pd.testing.assert_frame_equal(
            splitter_buyers_split_perc_df, 
            true_buyers_split_perc_df
            )
