"""The SplitBill class stores data on splitting the bill for each person.

The SplitBill class stores the receipt and the itemized cost for each person.
The SplitBill class stores the names of buyers 
and the amount each owe.

Typical usage example:

    purchases_csv = 'tests/data/true-CSTCO_2020-05-01.csv'
    costco_split_bill = SplitBill(purchases_csv, 'CSTCO', '2020-05')
    totals = costco_splitt_bill.totals
"""

import numpy as np
import pandas as pd
from src.receipt import Receipt

class SplitBill(Receipt):

    def __init__(self, purchases_data, store_name=None, yr_mo_str=None):
        super().__init__(purchases_data, store_name, yr_mo_str)

        self.receipt_columns = self.columns
        del self.columns

        self._set_purchases_df(purchases_data)
        self._set_result_df(self.purchases_df)
        self._set_meta_data(self.purchases_df)

    def _set_purchases_df(self, purchases_data):

        if isinstance(purchases_data, str):
            purchase_df = self._get_purchase_df_from_csv(purchases_data)
        elif isinstance(purchases_data, pd.core.frame.DataFrame):
            purchase_df = purchases_data  
        else:
            self._raise_parse_data_error(purchases_data)
        
        self.purchases_df = purchase_df

    def _get_purchase_df_from_csv(self, csv_path):
        
        if csv_path.endswith('.csv'):
            purchases_df = pd.read_csv(csv_path)

        elif csv_path.endswith('.xlsx'): 
            purchases_df = pd.read_excel(csv_path)

        return purchases_df
    
    def _raise_parse_data_error(self, purchases_data):

        raise TypeError(f'''
            Did not recognize receipt data {type(purchases_data)}. 
            Please input data as a pandas df or path to csv''')
    
    def _set_result_df(self, purchases_df):

        split_df = self._get_split_df(purchases_df)
        totals = self._get_totals(purchases_df)

        result_df = split_df.append(totals)
        result_df.index = result_df.index.astype(str)

        self.result_df = result_df

    def _get_totals(self, purchases_df):

        split_df = self._get_split_df(purchases_df).drop('product', axis=1)

        totals_ser = split_df.sum(axis=0).round(2)
        totals_ser.name = 'TOTAL'

        return totals_ser

    def _get_split_df(self, purchases_df):

        split_df = self._get_split_df(purchases_df)

        return split_df
    
    def _get_split_df(self, purchases_df):

        products_df = self._get_products_df(purchases_df)
        buyers_split_df = self._get_buyers_split_df(purchases_df)

        split_df = pd.concat([products_df, buyers_split_df], axis=1)

        return split_df
    
    def _get_products_df(self, purchases_df):

        product_df = purchases_df[['product', 'price']]
        return product_df

    def _get_buyers_split_df(self, purchases_df):
        
        buyers_only_df = (
            purchases_df.drop(['product', 'price'], axis=1).fillna(0)
            )
        buyers_split_perc_df = self._get_buyers_split_perc_df(buyers_only_df)
        buyers_split_df = buyers_split_perc_df.multiply(self.purchases_df['price'], axis=0)

        return buyers_split_df.round(2)

    def _get_buyers_split_perc_df(self, df):

        return df.div(df.sum(axis=1), axis=0)
    
    def _set_meta_data(self, purchases_df):
        
        self.totals = self._get_totals(purchases_df)
        self.buyers = purchases_df.drop(self.receipt_columns, axis=1).columns.tolist()



