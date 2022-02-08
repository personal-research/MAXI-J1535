'''

testing notes

1050360103_0
/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/1050360103/jspipe/js_ni1050360103_0mpu7_silver_GTI0-bin.pds

/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/post-processing/initial/pds_plots/with_pyxspec.py

'''


import numpy as np
import os
import pandas as pd

import xspec 
from xspec import *

from tqdm import tqdm 
import feather

def pyxspec_plot(): 
    import matplotlib.pyplot as plt

    all_ids = list(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/good_ids.csv')['full_id'])

    pds_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
    fak_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-fak.rsp'

    plot_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/post-processing/initial/pds_plots/plot_dir/plots'
    data_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw'

    # fix above two

    Xset.chatter = 0
    #Xset.logChatter = 10
    Fit.query = "no"

    for full_id in tqdm(all_ids): 
        id_list = full_id.split('_')
        obs_id = id_list[0]
        gti = id_list[1]

        pds_file = pds_temp.replace('+++', obs_id)
        pds_file = pds_file.replace('***', gti)


        from astropy.io import fits

        hdul = fits.open(pds_file)
        print(hdul[1].header['RESPFILE'])

        s1 = Spectrum(pds_file)

        # fix path of spectrum files! 

        s1.ignore('**-0.02')
        s1.ignore('100.-**')

        m1 = Model("loren+loren")

        m1.lorentz.LineE = 0
        m1.lorentz.LineE.frozen = True
        m1.lorentz_2.LineE = 0
        m1.lorentz_2.LineE.frozen = True

        Fit.perform()

        Plot.splashPage = False

        Plot.xAxis = "keV"
        Plot("data")

        log_path = data_dir + '/' + obs_id + '.ftr'
        plot_path = plot_dir + '/' + obs_id + '.png'
        
        x = Plot.x()
        y = Plot.y()
        xerr = Plot.xErr()
        yerr = Plot.yErr()

        plt.style.use("/mnt/c/Users/Research/Documents/GitHub/sunnyhills/other/aesthetics/science.mplstyle")
        fig, ax = plt.subplots(figsize=(5,3))

        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

        ax.scatter(x,y, s=3)
        ax.errorbar(x,y,yerr=yerr,xerr=xerr, lw=0,elinewidth=1)

        ax.set(xlim=(0.2,20), ylim=(10**-5,max(y)), xscale='log', yscale='log', 
               xlabel='Frequency [Hz]', ylabel='rms-Normalized Power')

        ax.fill_between([0.8,1.2],0,max(y),color='indianred',alpha=0.1)

        out_df = pd.DataFrame(list(zip(x,y,xerr,yerr)), columns=['x','y','xerr','yerr'])
        out_df.to_feather(log_path)

        plt.savefig(plot_path,dpi=150)
        plt.clf()
        plt.close()

pyxspec_plot()