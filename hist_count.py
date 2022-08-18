#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''python script to generate histograms comparing snow and no snow ρv ρg, parameters
    manually changed depending on data visualisation required'''

snow = pd.read_csv('/home/s2126572/DISSERTATION/data_processing/ph_rates/rate_sn.csv')
no_snow = pd.read_csv('/home/s2126572/DISSERTATION/data_processing/ph_rates/rate_no_sn.csv')

snow_op = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/old?/ph_rates_2/rate_snow_op.csv")
no_snow_op = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/old?/ph_rates_2/rate_no_snow_op.csv")

snow_forest = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_rates/rate_sn_forest_filt.csv")
no_snow_forest = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_rates/rate_no_sn_forest.csv")


x1 = snow['ρg']
x2 = no_snow['ρg']

l1 = ['snow -initial- ρg', 'no snow -initial- ρg']
c = ['#41aabf', '#117733']

plt.hist([x1, x2], bins = 25, alpha = 0.5, histtype= "bar", label= l1, edgecolor='grey', color = c , density=True, stacked = True)
plt.xticks(np.arange(0,13, step=0.5))
plt.xlabel('ρg')
plt.ylabel('density')

plt.legend(loc='upper right')
plt.show()
