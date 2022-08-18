import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

'''python script to generate histograms of total radiometric returns, parameters
    changed manually depending on results needed'''

ss_rates = pd.read_csv('/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/ss_rates.csv')

snow = pd.read_csv('/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/sn.csv')
no_snow = pd.read_csv('/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/no_sn.csv')

snow_day = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/filtered_scenes/snow_day.csv")
snow_night = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/filtered_scenes/snow_night.csv")
snow_power = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/filtered_scenes/snow_power.csv")
snow_weak = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/filtered_scenes/snow_weak.csv")
snow_atm = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/filtered_scenes/snow_atm.csv")

no_snow_day = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/filtered_scenes/no_snow_day.csv")
no_snow_night = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/filtered_scenes/no_snow_night.csv")
no_snow_power = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/filtered_scenes/no_snow_power.csv")
no_snow_weak = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/filtered_scenes/no_snow_weak.csv")
no_snow_atm = pd.read_csv("/home/s2126572/DISSERTATION/data_processing/ph_cnt_grp/filtered_scenes/no_snow_atm.csv")

snow_forest = pd.read_csv('/home/s2126572/DISSERTATION/data_processing/filtered_scenes/snow_forest.csv')
no_snow_forest = pd.read_csv('/home/s2126572/DISSERTATION/data_processing/filtered_scenes/no_snow_forest.csv')

clear = [0,1,2]
sn_atm = snow[~snow['msw'].isin(clear)]
no_sn_atm = no_snow[~no_snow['msw'].isin(clear)]

x1 = no_sn_atm['signal photon rate']
x2 = no_sn_atm['ρv_c']
x3 = no_sn_atm['ρg_c']
x4 = sn_atm['signal photon rate']
x5 = sn_atm['ρv_c']
x6 = sn_atm['ρg_c']

#colour scheme
grey = '#666686'
green = '#117733'
blue = '#88CCEE'
yellow = '#CCBA77'
purple = '#AA4499'
pink = '#820342'
cream = '#FDEFEF'
brown = '#9E8F7A'
grey2 = '#7D7D7D'
purple2 = '#5D3A9B'
orange = '#D47F41'


plt.figure()
''' comment and change parameters as necessary for plt.figure input'''

# plt.hist(x1, bins=200, label = 'No Snow MSW Flag Radiometry',  color = grey, edgecolor=brown, density=True, stacked = True)
# plt.hist(x3, bins=200, label = 'No Snow MSW Flag Ground Radiometry', alpha= 0.7, edgecolor = brown, color = yellow, density = True, stacked = True)
# plt.hist(x2, bins=30, label = 'No Snow MSW Flag Canopy Radiometry', alpha = 0.6, edgecolor = brown, color = green, density = True, stacked = True)

# plt.hist(x4, bins=250, label = 'Snow MSW Flag Radiometry',  color = cream, edgecolor=brown, density=True, stacked = True)
# plt.hist(x6, bins=250, label = 'Snow MSW Flag Ground Radiometry', alpha= 0.7, edgecolor = brown, color = purple, density = True, stacked = True)
# plt.hist(x5, bins=100, label = 'Snow MSW Flag Canopy Radiometry', alpha = 0.6, edgecolor = brown, color = blue, density = True, stacked = True)

plt.xlabel('Radiometric returns photons/shot')
plt.ylabel('Density')
plt.title('snow - MSW Flag radiometry')
plt.legend(loc ="upper right")
plt.xlim(0,16)
plt.ylim(0,2)

plt.show()
