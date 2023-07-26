# import from built-in modules 
from argparse import ArgumentParser, RawTextHelpFormatter as RT
from datetime import date, datetime
from pathlib  import Path

import numpy as np
import matplotlib.pyplot as plt

# import from personal modules 
from utils.dfModifier import modify_df_real, modify_df_sim

FPATH = Path(__file__)
DIR = FPATH.parent

def getArguments():
    ''' parse the command-line interface
        the command line takes four required arguments  

        ipt: the directory including the .out files to be plotted
        opt: the directory to output the overlay plot(s)) 
    '''  
    parser = ArgumentParser(formatter_class=RT)
    parser.add_argument('ipt', type = str, help="the directory including the .out files to be plotted")
    parser.add_argument('opt', type = str, help="the directory to store the overlay plot")

    return parser.parse_args()

def main():
    ''' the basic structure of the python scripts '''  
    args = getArguments()

    ipt = DIR.joinpath(args.ipt)
    opt = DIR.joinpath(args.opt)
    
    # add other required files to out directory 
    files = Path(ipt).glob('*.out')
    for f in files:
        cp(f, opt)

if __name__ == "__main__":
    main()
