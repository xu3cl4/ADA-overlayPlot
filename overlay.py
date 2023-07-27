# import from built-in modules 
from argparse import ArgumentParser, RawTextHelpFormatter as RT
from datetime import date, datetime
from pathlib  import Path

import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd

# import from personal modules 
from utils.dfModifier import modify_df_real, modify_df_sim
from utils.others     import getIndices

FPATH = Path(__file__)
DIR = FPATH.parent

attributes = ['Tritium', 'Uranium', 'Aluminum', 'pH', 'Depth to water']
units = {
        'Tritium': 'kg/mol', 'Uranium': 'kg/mol', 
        'Aluminum': 'kg/mol', 'pH': None, 'Depth to water': 'ft'
        }

wells = { 95: 'FSB95DR', 110: 'FSB110D'}

def getArguments():
    ''' parse the command-line interface
        the command line takes four required arguments  

        ipt: the directory including the .out files to be plotted
        opt: the directory to output the overlay plot(s)) 
    '''  
    parser = ArgumentParser(formatter_class=RT)
    parser.add_argument('ipt_real', type = str, help="the file path to the real observations")
    parser.add_argument('ipt_sim',  type = str, help="the directory including the .out files to be plotted")
    parser.add_argument('opt',      type = str, help="the file path to store the overlay plot")
    parser.add_argument('well',     type = int, help="95 or 110")

    return parser.parse_args()

def main():
    ''' the basic plotting structure of the python scripts '''  
    args = getArguments()

    ipt_real = DIR.joinpath(args.ipt_real)
    ipt_sim  = DIR.joinpath(args.ipt_sim)
    opt      = DIR.joinpath(args.opt)
    well     = args.well
  
    # create a frame of subplots 
    nrow, ncol = 2, 3
    fig, axs = plt.subplots(nrow, ncol, sharex=True)


    # plot real observations with labels, legends  
    ob = pd.read_csv(ipt_real)
    ob = modify_df_real(ob)
    for i, attribute in enumerate(attributes):
        r, c = getIndices(i, ncol)

        # labels
        unit = units[attribute]
        axs[r,c].set(xlabel=None, ylabel=f"{attribute}{' (' + unit + ')' if unit else ''}")
            
        # observations
        axs[r,c].plot(ob["COLLECTION_DATE"], ob[attribute.lower()], ls='dotted', ms=1, color='blue', label="observations")

        # legend 
        if r + c == 0: # only need one legend
            axs[r,c].legend(loc=1)
        

    # plot simulated data 
    files = Path(ipt_sim).glob('*.out')
    for f in files:
        sim = pd.read_csv(f, skiprows=2)
        print(sim.to_string())
        # change column types, choose the points in the desired wells 
        # end up with the columns: region, variable, time, value
        sim = modify_df_sim(sim, well)

        for i, attribute in enumerate(attributes):
            r, c = getIndices(i, ncol)
            sim_attr = sim[sim['variable'] == attribute.lower()]
            sim_attr = sim_attr.pivot(index="time", columns="region", values="value")
            sim_attr_avg = sim_attr.mean(axis=1)
            dates = (sim_attr_avg.index).to_series()
            values = (sim_attr_avg.to_frame())[0]
            axs[r,c].plot(dates, values)

    fig.suptitle(f'{wells[well]}')
    fig.savefig(opt)

if __name__ == "__main__":
    main()
