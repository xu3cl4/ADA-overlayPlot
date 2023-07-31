# import from built-in modules 
from argparse import ArgumentParser, RawTextHelpFormatter as RT
from datetime import date, datetime
from math     import inf
from pathlib  import Path

import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd

# import from personal modules 
from utils.dfModifier import modify_df_real, modify_df_sim
from utils.others     import getIndices

FPATH = Path(__file__)
DIR = FPATH.parent

attributes_95 = ['Tritium', 'Uranium', 'Aluminum', 'pH', 'Depth to water']
attributes_110 = ['Tritium', 'Uranium', 'pH', 'Depth to water']
units = {
        'Tritium': 'mol/kg', 'Uranium': 'mol/kg', 
        'Aluminum': 'mol/kg', 'pH': None, 'Depth to water': 'ft'
        }

wells = {95: 'FSB95DR', 110: 'FSB110D'}
attributes_sets = {95: attributes_95, 110: attributes_110}

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
    nrow, ncol = 2, 3 if well == 95 else 2
    fig, axs = plt.subplots(nrow, ncol, sharex=True)


    # plot real observations with labels, legends  
    ob = pd.read_csv(ipt_real)
    ob = modify_df_real(ob)
    for i, attribute in enumerate(attributes_sets[well]):
        r, c = getIndices(i, ncol)

        # labels
        unit = units[attribute]
        axs[r,c].set_xlabel(None)
        axs[r,c].set_ylabel(f"{attribute}{' (' + unit + ')' if unit else ''}", fontsize=10)
        axs[r,c].tick_params(labelrotation=45, labelsize=6)
            
        # observations
        axs[r,c].scatter(ob["COLLECTION_DATE"], ob[attribute.lower()], color='blue', label="observations", zorder=inf, s=1)

        # legend 
        if r + c == 0: # only need one legend
            axs[r,c].legend(prop = {'size':6}, loc=1)
        

    # plot simulated data 
    files = Path(ipt_sim).glob('*.out')
    for f in files:
        sim = pd.read_csv(f, skiprows=2)
        # change column types, choose the points in the desired wells 
        # end up with the columns: region, variable, time, value
        sim = modify_df_sim(sim, well)

        for i, attribute in enumerate(attributes_sets[well]):
            r, c = getIndices(i, ncol)
            sim_attr = sim[sim['variable'] == attribute.lower()]
            sim_attr = sim_attr.pivot(index="time", columns="region", values="value")
            sim_attr_avg = sim_attr.mean(axis=1)
            dates = (sim_attr_avg.index).to_series()
            values = (sim_attr_avg.to_frame())[0]
            axs[r,c].plot(dates, values)

    fig.suptitle(f'{wells[well]}', y=0.95)
    fig.tight_layout()
    
    if well == 95: fig.delaxes(axs[1,2]) 
    
    fig.savefig(opt)

if __name__ == "__main__":
    main()
