import pytest
import numpy as np
import pandas as pd
import sys
import os
from src.split_costs import SplitBill

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