# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 15:52:44 2017

@author: Anu
"""


import pandas as pa, glob, os
    
df = pa.concat(map(pa.read_csv, glob.glob(os.path.join("", "iowa_*.csv"))), ignore_index=True)
df.columns = ['dom', 'doy', 'mnth', 'yr', 'pcp']
s_val_data = []
for index,row in df.iterrows():
    if (index + 15) <= len(df):
        s_val = "S_" + str(int(row[2])) + "/" + str(int(row[0])) + "/" + str(int(row[3]))
        subset_ix = range(index, index + 15)
        s_val_data.append([s_val, df.iloc[subset_ix]['pcp'].sum()])
s_val_df = pa.DataFrame(s_val_data)
s_val_df.columns = ['s_val', 'pcp_sum']
s_val_df['c_val'] = 0
s_val_df.loc[s_val_df['pcp_sum'] >= s_val_df['pcp_sum'].quantile(0.95), 'c_val'] = 1
print s_val_df
s_val_df.to_csv("c_label.csv")
