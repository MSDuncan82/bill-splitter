"""The Receipt class stores a pandas DataFrame of products & purchases.

The Receipt class stores data in the correct format of products & purchases.
It handles inputs as a csv path or pandas df.

Typical usage example:

    purchases_csv = 'tests/data/true-CSTCO_2020-05-01.csv'
    cstco_receipt = Receipt(purchases_csv, 'CSTCO', '2020-05')
"""

import numpy as np
import pandas as pd

class Receipt(object):

    def __init__(self, receipt_data, store_name=None, yr_mo_str=None):
        
        self.columns = ['product', 'price']

        self._set_receipt_df(receipt_data)
        self._set_store_name(store_name)
        self._set_yr_mo_str(yr_mo_str)
    
    def __repr__(self):

        return self.receipt_df
    
    def _set_store_name(self, store_name):

        self.store_name = None

        if store_name is not None:
            if isinstance(store_name, str):
                self.store_name = store_name
            else:
                raise TypeError(f'''
                Cannot set store name with type: {type(store_name)}. Use str''')

    def _set_yr_mo_str(self, yr_mo_str):
        
        self.yr_mo_str = None

        if yr_mo_str is not None:
            if isinstance(yr_mo_str, str):
                self.yr_mo_str = yr_mo_str
            else:
                raise TypeError(f'''
                Cannot set date with type: {type(yr_mo_str)}. Use str''')

    def _set_receipt_df(self, receipt_data):

        if isinstance(receipt_data, str):
            self._set_receipt_df_from_csv(receipt_data)
        elif isinstance(receipt_data, pd.core.frame.DataFrame):
            self._set_receipt_df_from_df(receipt_data)  
        else:
            self._raise_parse_data_error(receipt_data)

    def _set_receipt_df_from_csv(self, csv_path):

        self.receipt_df = pd.read_csv(csv_path, usecols=self.columns)

    def _set_receipt_df_from_df(self, receipt_df):

        for col in self.columns:
            if col not in receipt_df.columns:
                raise ValueError(f'''
                Receipt DataFrame needs columns {self.columns}.
                ''')

        self.receipt_df = receipt_df[self.columns]
    
    def _raise_parse_data_error(self, receipt_data):

        raise TypeError(f'''
            Did not recognize receipt data {type(receipt_data)}. 
            Please input data as a pandas df or path to csv 
            with columns {self.columns}''')

