#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import glob
import argparse
import os
import geopandas as gpd
from shapely.geometry import box

'''python script to clip radiometric rates to study site and merge with snow snow_scene
    classifications to stratify data to snow, no snow, and variable snow .csv files'''

def getCmdArgs():

    parser = argparse.ArgumentParser()

    parser.add_argument("ph_cnt_file", help = "file path directory containing photon count csv files")
    parser.add_argument("ss_file", help = "snow scene file path directory (csv file format)")
    parser.add_argument("outfile", help = "file path directory for output files folder")

    args = parser.parse_args()

    return args

def clip_tracks(rates_df):
    '''clips extent of dataframe to identified bounding box for study area, producing geodataframe POINT data'''
    geo_output = gpd.GeoDataFrame(rates_df, geometry=gpd.points_from_xy(rates_df.longitude, rates_df.latitude))
    geo_output = geo_output.set_crs('epsg:4326')
    bbox = box(26.30,66.89,27.39,67.89)
    rates_sod = geo_output.clip(bbox)
    rates_sod.to_csv(outfile_path + '_sod' + '.csv')

    return(rates_sod)

def merge_ss(rates_sod, snow_scene, outfile_path):
    '''combines study site rates and ICESat-2 metrics with external snow scene evaluation'''
    ss_rates = snow_scene.merge(rates_sod, how='right', on='date')
    ss_rates.rename(columns = {'noise reduced canopy photon rate':'ρv_c','ground photon rate':'ρg_c', 'beam strength': 'strong', 'night flag': 'night'}, inplace=True)
    ss_rates = ss_rates.drop(ss_rates.columns[[2]], axis=1)
    ss_rates['ρv_c'] = ss_rates['ρv_c'].fillna(0)
    ss_rates = ss_rates.astype({'date' : str})
    ss_rates = ss_rates.astype({'night': bool})

    ss_rates.to_csv(os.path.join(outfile_path +'/ss_rates.csv'))
    print(ss_rates)

    return ss_rates


def filter_scene(ss_rates, outfile_path):
    '''Returns filtered CSV file inputs for input into Matt Purslow code'''

    no_sn = (pd.DataFrame(ss_rates.loc[ss_rates['type'] == 0]))
    no_sn.to_csv(os.path.join(outfile_path + '/no_sn.csv'))
    sn = (pd.DataFrame(ss_rates.loc[ss_rates['type'] == 1]))
    sn.to_csv(os.path.join(outfile_path + '/sn.csv'))
    var_sn = (pd.DataFrame(ss_rates.loc[ss_rates['type'] == 2]))
    var_sn.to_csv(os.path.join(outfile_path + '/var_sn.csv'))

    return no_sn, sn, var_sn


if __name__ == '__main__':

    cmd = getCmdArgs()
    path = cmd.ph_cnt_file
    ss_file = cmd.ss_file
    outfile = cmd.outfile

#photon count files to concatenate

    csv_files = glob.glob(path + "/*.csv")
    df_list = (pd.read_csv(file) for file in csv_files)
    rates_df  = pd.concat(df_list, ignore_index=True)

#snow scene file to merge with all photon count files
    snow_scene = pd.read_csv(ss_file)
    snow_scene =  snow_scene.replace("-","", regex = True)
    snow_scene['date']=snow_scene['date'].astype(int)

# outfile path

    outfile_path = os.path.join(outfile + "/ph_cnt_grp")
    if not os.path.exists(outfile_path):
        os.mkdir(outfile_path)


#call functions

    rates_sod = clip_tracks(rates_df)
    ss_rates = merge_ss(rates_sod, snow_scene,outfile_path)
    filter_scene(ss_rates, outfile_path)
