import numpy as np 
import pandas as pd 
from helpers import *

import warnings 
warnings.filterwarnings('ignore')

predicted = pd.read_csv('predicted.csv')

## Too good to be true? NO IT WORKS

recs = recommend_songs([{'name': 'Come As You Are', 'year':1991},
                {'name': 'Smells Like Teen Spirit', 'year': 1991},
                {'name': 'Lithium', 'year': 1992},
                {'name': 'All Apologies', 'year': 1993},
                {'name': 'Stay Away', 'year': 1993}],  predicted)


print(len(recs))