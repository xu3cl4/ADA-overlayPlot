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
    paresr.add_argument('well',     type = int, help="95 or 110")

    return parser.parse_args()

def main():
    ''' the basic structure of the python scripts '''  
    args = getArguments()

    ipt_real = DIR.joinpath(args.ipt_real)
    ipt_sim  = DIR.joinpath(args.ipt_sim)
    opt      = DIR.joinpath(args.opt)
    well     = args.well
  
    # create a frame of subplots 
    nrow, ncol = 2, 3
    fig, axs = plt.subplots(nrow, ncol, sharex=True)

    # plot real observations 
    with open('ipt_real', 'r') as f:
        for i, attribute in enumerate(attributes):
            r, c = getIndices(i, ncol)
        
    # plot simulated data 
    files = Path(ipt).glob('*.out')
    for fname in files:
        with open(fname, 'r') as f:
            for i, attribute in enumerate(attributes):
                r, c = getIndices(i, ncol)

    fig.savefig(opt)

if __name__ == "__main__":
    main()
