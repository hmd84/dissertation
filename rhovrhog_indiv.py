#!/usr/bin/env python
# coding: utf-8
""" Pared down function to calculate best-fit ρv/ρg for ICESat-2 segments.

    Requires as input pandas dataframe seg with:
    Date (string): 'date'
    Ground track (string): 'gtx'
    Ground photon rate (float): 'ρg_c'
    Canopy photon rate (float): 'ρv_c'
    Strong beam identifier (boolean): 'strong'
    Nighttime identifier (boolean): 'night'
    rhovrhog.py file provided by Matt Purslow
    Hazel Davies edits noted with 'HD'
    """
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = 'Arial'
from matplotlib.cm import gist_earth as cmap
import h5py
import argparse
import os


def getCmdArgs():
    ''' HD command line arguments for linux terminal'''
    parser = argparse.ArgumentParser()

    parser.add_argument("infile", help = "file path containing reflectance rates for analysis (ie. ss_rates, no_snow, snow) as .csv")
    parser.add_argument("name", help = "desired file name corresponding to infile")
    parser.add_argument("outfile", help = "file directory for folder location of outputs")

    args = parser.parse_args()

    return args


def fit(seg):
  """ Identify individual tracks and perform regression for site """
  ## Label segments with track identifier
  seg['track'] = [str(d)+str(g) for d, g in zip(seg.date, seg.gtx)]
  ## Calculate R² for each track
  seg = getWeights(seg)
  print(seg)
  ## Identify tracks with more than 1 segment
  tracks = np.unique(seg.track.values)
  keep = [seg.loc[seg.track==t].shape[0] > 1 for t in tracks]
  tracks = tracks[keep]
  seg = seg.loc[np.isin(seg.track, tracks)]
  ## Assign track index to each track (for least_squares parameter array)
  iTrack = np.full(seg.shape[0], -999)
  for t in range(tracks.shape[0]):
    i = np.argwhere(seg.track.values==tracks[t])
    iTrack[i] = t
  seg['trackIndex'] = iTrack
  ## Calculate fit
  rate = getODR(seg, tracks)
  ## Return DataFrame with calculated rates
  return rate


def getWeights(seg):
  """ Calculate R² values for ICESat-2 tracks """
  ## Assign initial weight as zero (will be excluded from fit)
  seg['weight'] = 0.
  for track in np.unique(seg.track.values):
    ## Calculate R² for track
    R = seg.loc[seg.track==track][['ρg_c', 'ρv_c']].corr().values[0,1]
    print(R)
    ## If negatively correlated
    if R < -0.5:
      ## Assign non-zero weighting to all segments in track
      seg.loc[seg.track==track, 'weight'] = R**2.

  return seg



def getODR(seg, tracks):
  """ Perform least-squares regression using Orthogonal Distance Regression """
  ## Create initial estimates of slope m for site and y-intercepts c for each track
  Nt = tracks.shape[0]
  mc_init = np.full(Nt+1, 1.)
  mc_init[-1:] = -1.
  m_est = []
  for i in range(Nt):
    segs = seg.loc[seg.track==tracks[i]]
    ρv_est = segs.ρv_c.max()
    ρg_est = segs.ρg_c.max()
    m_est.append(-(ρv_est/ρg_est))
    mc_init[i] = ρv_est
  mc_init[-1] = np.mean(m_est)
  ## Perform least squares regression finding Levenberg-Marquardt solution
  result = least_squares(func, mc_init, method='lm',
                         args=(seg.ρg_c, seg.ρv_c, seg.strong,
                               seg.trackIndex, seg.weight, False))
  m_fit = result.x[-1]
  c_fit = result.x[:-1]
  ## Pack results into output dataframe
  rate = pd.DataFrame()
  rate['track'] = tracks
  rate['date'] = [t[:8] for t in rate.track.values]
  rate['gtx'] = [t[8:] for t in rate.track.values]
  rate['strong'] = [seg.loc[seg.track==t].strong.max()                     for t in rate.track.values]
  rate['night'] = [seg.loc[seg.track==t].night.max()                    for t in rate.track.values]
  rate['ρv'] = c_fit
  rate['ρg'] = -rate.ρv / m_fit
  rate['weight'] = seg.groupby('track').mean().weight.loc[rate.track.values].values
  rate['ρvρg'] = rate.ρv / rate.ρg
  return rate


def func(mc, ρg, ρv, s, t, w, split):
  """ Function to find weighted orthogonal distance residuals """
  ## Create empty array to hold residuals
  res = []
  ## For each segment
  for ρgi, ρvi, si, ti, wi in zip(ρg, ρv, s, t, w):
    ## Find orthogonal distance residual for segment
    d, x0, y0 = orthodist(ρgi, ρvi, mc[-1], mc[ti])
    ## Weight residual
    res.append(d*wi)
  ## Return array of residuals
  return np.array(res)

def orthodist(ρg, ρv, m, c):
  """ Function to find orthogonal distance from point to line """
  ## Calculate orthogonal distance
  d = np.abs((m*ρg)-ρv+c) / np.sqrt((m**2.)+1.)
  ## Assign sign correctly
  if ρv < ((m*ρg) + c):
    d = -d
  ## Locate nearest points on line
  x0 = (-1.*((-1.*ρg) - (m*ρv)) - (m*c)) / (m**2 + 1)
  y0 = (m*x0) + c
  return d, x0, y0


def plot(seg, rate):
  """ Plot scatter plot with fitted lines, coloured by track """
  fig = plt.figure(figsize=(4,3.5)); ax = fig.gca(); plt.title('')
  ## Plot segments and fit for each track
  Ntrack = rate.shape[0]
  for t in range(Ntrack):
    s = seg.loc[seg.date+seg.gtx==rate.track.values[t]]
    r = rate.loc[rate.track==rate.track.values[t]]
    c = color=cmap(t/(1.1*Ntrack))
    ax.scatter(s.ρg_c, s.ρv_c, color=c, s=1)
    ax.plot([0, r.ρg], [r.ρv, 0], color=c, lw=1)
  ## Label axes
  ax.set_xlabel('$ρ_{gc}$ (shot$^{-}$¹)')
  ax.set_ylabel('$ρ_{vc}$ (shot$^{-}$¹)')
  ## Normalise formatting on x and y axes
  ax.set_aspect('equal')
  # axMax = np.ceil([ax.get_xlim()[1], ax.get_ylim()[1]]).max()
  axMax = np.ceil([ax.get_xlim()[1], ax.get_ylim()[1]]).max()
  ax.set_xlim(0,axMax); ax.set_ylim(0,axMax)
  ax.set_xticks(np.arange(0,axMax+.1,1.))
  ax.set_yticks(np.arange(0,axMax+.1,1.))
  ## Clean up and show
  fig.tight_layout()
  fig.show()


if __name__ == '__main__':
    ''' HD define command line arguments use and read .csv files to dataframes in
    appropriate data formats'''
    cmd = getCmdArgs()

    infile = cmd.infile
    name = cmd.name
    outfile = cmd.outfile

    ss_rates = pd.read_csv(infile)
    ss_rates = ss_rates.fillna(0)
    ss_rates = ss_rates.astype({'date' : str})


    seg = ss_rates
    seg = ss_rates[ss_rates['ρv_c']<2]
    seg = ss_rates[ss_rates['ρg_c']<2]
    print(seg)

    outfile_path = (outfile + "/ph_rates")
    if not os.path.exists(outfile_path):
        os.mkdir(outfile_path)

    output_file = (os.path.join(outfile_path, 'rate_' + name + '.csv'))
    output_png = (os.path.join(outfile_path, 'rate_' + name + '.png'))

    # Calculate fit
    rate = fit(seg)
    ## Show calculated rates
    print(rate)
    ## Plot scatter plot
    plot(seg, rate)

    rate.to_csv(output_file)
    plt.savefig(output_png)
