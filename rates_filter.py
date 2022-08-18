import pandas as pd
import argparse
import os

'''python script filtering snow and no snow data for consideriation of optimum
    aquisition conditions and ground classifications'''

def getCmdArgs():

    parser = argparse.ArgumentParser()

    parser.add_argument("infile", help = "file location of csv file containing all segment metrics (ss_rates)")
    parser.add_argument("outfile", help = "file directory for folder location of outputs")
    parser.add_argument("snl_infile", help = "snow file containing appended land classification values for each photon event")
    parser.add_argument("nsnl_infile", help = "no snow file containing appended land classification values for each photon event")

    args = parser.parse_args()

    return args

def optimum_aq(snow, no_snow, outfile_path):
    '''filters based on optimum aquisition identification'''

    snow_power = snow.loc[snow['strong'] == True]
    snow_power.to_csv(outfile_path + '/snow_power.csv')
    snow_weak = snow.loc[snow['strong'] == False]
    snow_weak.to_csv(outfile_path + '/snow_weak.csv')

    no_snow_power = no_snow.loc[no_snow['strong'] == True]
    no_snow_power.to_csv(outfile_path + '/no_snow_power.csv')
    no_snow_weak = no_snow.loc[no_snow['strong'] == False]
    no_snow_weak.to_csv(outfile_path + '/no_snow_weak.csv')

    snow_day = snow.loc[snow['night'] == False]
    snow_day.to_csv(outfile_path + '/snow_day.csv')
    snow_night = snow.loc[snow['night'] == True]
    snow_night.to_csv(outfile_path + '/snow_night.csv')

    no_snow_day = no_snow.loc[no_snow['night'] == False]
    no_snow_day.to_csv(outfile_path + '/no_snow_day.csv')
    no_snow_night = no_snow.loc[no_snow['night'] == True]
    no_snow_night.to_csv(outfile_path + '/no_snow_night.csv')

    clear = [0,1,2]

    snow_atm = snow[snow['msw'].isin(clear)]
    snow_atm.to_csv(outfile_path + '/snow_atm.csv')
    no_snow_atm = no_snow[no_snow['msw'].isin(clear)]
    no_snow_atm.to_csv(outfile_path + '/no_snow_atm.csv')

    #optimum conditions filter
    snow_op_con = snow[(snow['strong'] == True) & (snow['night'] == True) & (snow['msw'].isin(clear))]
    snow_op_con.to_csv(outfile_path + '/snow_op.csv')
    no_snow_op_con = no_snow[(no_snow['strong'] == True) & (no_snow['night'] == True) & (no_snow['msw'].isin(clear))]
    no_snow_op_con.to_csv(outfile_path + '/no_snow_op.csv')


def ground_filter(snow_land, no_snow_land, outfile_path):
    '''filters out all non-forest land classifications'''
    surface = [20,30,50,80,90,126,121]

    snow_land_filt_ex = snow_land[~snow_land['DN'].isin(surface)]
    snow_land_filt_ex.to_csv(outfile_path + '/snow_lc_forest.csv')
    no_snow_land_filt_ex = no_snow_land[~no_snow_land['DN'].isin(surface)]
    no_snow_land_filt_ex.to_csv(outfile_path + "/no_snow_lc_forest.csv")

if __name__ == '__main__':

    cmd = getCmdArgs()

    infile = cmd.infile
    outfile = cmd.outfile
    snl_infile = cmd.snl_infile
    nsnl_infile = cmd.nsnl_infile

    outfile_path = os.path.join(outfile + "/filtered_scenes")
    if not os.path.exists(outfile_path):
        os.mkdir(outfile_path)

    df = pd.read_csv(infile)
    snow = df.loc[df['type'] == 1]
    no_snow = df.loc[df['type'] == 0]

    snow_land = pd.read_csv(snl_infile)
    no_snow_land = pd.read_csv(nsnl_infile)


    print(snow)
    print(no_snow)

    optimum_aq(snow, no_snow, outfile_path)
    ground_filter(snow_land, no_snow_land, outfile_path)
