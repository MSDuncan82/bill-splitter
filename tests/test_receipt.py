import pytest
import numpy as np
import pandas as pd
import sys
import os
from src.receipt import Receipt

TRUE_PURCHASES_CSV = 'tests/data/true-CSTCO_2020-05-01.csv'
TRUE_PURCHASES_DF = pd.read_csv(TRUE_PURCHASES_CSV)
TRUE_RECEIPT_DF = pd.read_csv(
            TRUE_PURCHASES_CSV, 
            usecols=['product', 'price'])

WRONG_COLS_CSV = 'tests/data/wrong-cols-CSTCO_2020-05-01.csv'
WRONG_PURCHASES_DF = pd.read_csv(WRONG_COLS_CSV)
WRONG_COLS_DF = pd.read_csv(
            WRONG_COLS_CSV, 
            usecols=['products', 'prices'])


class TestReceiptDF(object):

    @pytest.mark.parametrize(('receipt_data'), [TRUE_PURCHASES_CSV, TRUE_PURCHASES_DF])
    def test_correct_receipt(self, receipt_data):
        test_receipt = Receipt(receipt_data) 

        pd.testing.assert_frame_equal(
            TRUE_RECEIPT_DF,
            test_receipt.receipt_df
            )
    
    @pytest.mark.parametrize(('receipt_data'), [WRONG_COLS_CSV, WRONG_COLS_DF])
    def test_wrong_cols_receipt_df(self, receipt_data):
        with pytest.raises(ValueError):
            Receipt(receipt_data) 
    
    def test_wrong_type(self):
        with pytest.raises(TypeError):
            Receipt({'products':1})

class TestReceiptMeta(object):

    @pytest.mark.parametrize(('store_name'), [None, 'CSTCO', 'costco'])
    def test_correct_store_name(self, store_name):
        test_receipt = Receipt(TRUE_PURCHASES_CSV, store_name=store_name)

        assert test_receipt.store_name == store_name
    
    @pytest.mark.parametrize(('store_name'), [1, 0, [], {1, 4}])
    def test_incorrect_store_name(self, store_name):
        with pytest.raises(TypeError):
            Receipt(TRUE_PURCHASES_CSV, store_name=store_name)

    @pytest.mark.parametrize(('yr_mo_str'), [None, '2020-05', '2020-01'])
    def test_correct_yr_mo_str(self, yr_mo_str):
        test_receipt = Receipt(TRUE_PURCHASES_CSV, yr_mo_str=yr_mo_str)

        assert test_receipt.yr_mo_str == yr_mo_str
    
    @pytest.mark.parametrize(('yr_mo_str'), [1, 0, [], {1, 4}])
    def test_incorrect_yr_mo_str(self, yr_mo_str):
        with pytest.raises(TypeError):
            Receipt(TRUE_PURCHASES_CSV, yr_mo_str=yr_mo_str)