"""Splits an itemized receipt between multiple people

The BillSplitter class can split an itemized bill between multiple people.
It can either split all items evenly or take in a list of purchase ids per
person. If given a list of purchase ids it will split each item's cost for 
only the people that bought it.

Typical usage example:

    splitter = BillSplitter(purchases_df)
    result_df = splitter.get_result_df()
"""

import numpy as np
import pandas as pd

class BillSplitter(object):

    def __init__(self, purchases_df):

        self.purchases_df = purchases_df
    
    def get_result_df(self):

        split_df = self.get_split_df()
        totals = self.get_totals()

        result_df = split_df.append(totals)

        return result_df

    def get_totals(self):

        split_df = self.get_split_df().drop('product', axis=1)

        totals_ser = split_df.sum(axis=0)
        totals_ser.name = 'TOTAL'

        return totals_ser

    def get_split_df(self):

        products_df = self._get_products_df(self.purchases_df)
        buyers_split_df = self._get_buyers_split_df(self.purchases_df)

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
            
if __name__ == '__main__':

    purchases_df = pd.read_csv('data/example.csv')
    splitter = BillSplitter(purchases_df)
    split_df = splitter.get_split_df()
    totals = splitter.get_totals() 
    result_df = splitter.get_result_df()

