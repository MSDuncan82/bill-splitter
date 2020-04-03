import pandas as pd

class CSVGenerator(object):

    def __init__(self, purchases_dict=None, buyers_dict=None):
        
        pass
        # if purchases_dict is None and buyers_dict is None:
        #     purchases_dict, buyers_dict = self._get_purchases_and_buyers_dict()

        # if purchases_dict is None:
        #     purchases_dict = self._get_purchases_dict()
        
        # if buyers_dict is None:
        #     buyers_dict = self._get_buyers_dict()
    
    def _get_purchases_dict(self):

        purchases_dict = {}
        while True:
            item_str = input('Input item name (type "done" to finish): ')
            if item_str.lower() == 'done': break

            item_price = input('Input item price: $')
            item_price = round(float(item_price), 2)

            i = 1
            item_str_new = item_str
            while item_str_new in purchases_dict:
                item_str_new = f'{item_str}({i})'
                i += 1
            item_str = item_str_new

            purchases_dict.update({item_str:item_price})
        
        return purchases_dict