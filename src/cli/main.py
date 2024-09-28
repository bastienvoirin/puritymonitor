"""
Utility functions which are common to all CLI commands.
"""

####################################################################################################

import argparse
from itertools import permutations
from matplotlib import pyplot as plt

####################################################################################################

def printArgs(args):
    """
    Print a formatted summary of the arguments.
    """
    print("╔" + "═"*62 + "╗")
    print("║" + " "*15 + f"{'puritymonitor command-line interface': <38}" + " "*15 + "║")
    print("║" + " "*15 + f"{'   released under the MIT License   ': <38}" + " "*15 + "║")
    print("╠" + "═"*62 + "╣")
    
    for key, val in vars(args).items():
        if key == "input_files":
            print(f"║ {key+' ':.<17} [", end = "")
            print(*[f"{v+', ': <34} {' ': <6} ║\n║ {' ': <17}  " for v in val[:-1]], sep = "", end = "")
            if len(val) > 0:
                print(f"{val[-1]+'] ':.<34} {type(val).__name__: <6} ║")
            else:
                print(f"{'] ':.<34} {type(val).__name__: <6} ║")
        else:
            print(f"║ {key+' ':.<17} {str(val)+' ':.<35} {type(val).__name__: <6} ║")
            
    print("╚" + "═"*62 + "╝")
    return

####################################################################################################

def getFigs(nPurityMonitors: int, args):
    """
    """
    figs = {}
    print()
    
    # These nested `for` loops iterate over all figure combinations
    for nRows in range(1, len("sdg") + 1):
        for fig in permutations("sdg", nRows):
            if fig[0] == "g":
                title = "PM TPC geometries"
                if "s" in fig or "d" in fig:
                    title += " and energy spectra"
            else:
                title = "Energy spectra"
                if "g" in fig:
                    title += " and PM TPC geometries"
                    
            arg = "_".join(fig).replace("g", "geom").replace("s", "simu").replace("d", "data")
            fig = "".join(fig)
            
            print(f"{'>' if vars(args)[arg] else ' '}", f"{fig: <3}", f"{arg: <15}", f"{nRows: <3}", title)
            
            if vars(args)[arg]:
                figs[fig] = (plt.figure(title, figsize = (6 * nPurityMonitors, 4 * nRows)), arg)
                plt.get_current_fig_manager().set_window_title(title)  
    return nPurityMonitors, figs

####################################################################################################

def getSubplots(nPurityMonitors: int, figs):
    """
    All subplot logic/tiling is done by this generator function, which generates subplots for
    simulation, experimental data, and/or geometry for each purity monitor TPC length.
    """

    data = ([(key, len(key), key.index("d")) for key in figs.keys() if "d" in key], {})
    simu = ([(key, len(key), key.index("s")) for key in figs.keys() if "s" in key], {})
    geom = ([(key, len(key), key.index("g")) for key in figs.keys() if "g" in key], {"projection": "3d"})
    
    print()
    print(f"{'data:': <11}", data)
    print(f"{'simu:': <11}", simu)
    print(f"{'geom:': <11}", geom)
    
    for index in range(nPurityMonitors):
        for x, kwargs in (data, simu, geom):
            yield [
                (figs[fig][0], figs[fig][0].add_subplot(rows, nPurityMonitors, index + nPurityMonitors * row, **kwargs), row)
                for fig, rows, row in x
            ]