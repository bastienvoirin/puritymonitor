"""
Utility functions which are common to all CLI commands.
"""

####################################################################################################

from argparse import ArgumentParser
from itertools import permutations
from matplotlib import pyplot as plt

####################################################################################################

def createParser() -> ArgumentParser:
    """
    Create an argument parser for a CLI command.
    """

    parser = ArgumentParser()

    # Figures:

    parser.add_argument("-d", "--data", help = "plot data", action="store_true")
    parser.add_argument("-g", "--geom", help = "plot geometry", action="store_true")
    parser.add_argument("-s", "--simu", help = "plot simulation", action="store_true")

    parser.add_argument("-dg", "--data-geom", help = "plot data and geometry", action="store_true")
    parser.add_argument("-gd", "--geom-data", help = "plot geometry and data", action="store_true")
    parser.add_argument("-ds", "--data-simu", help = "plot data and simulation", action="store_true")
    parser.add_argument("-sd", "--simu-data", help = "plot simulation and data", action="store_true")
    parser.add_argument("-gs", "--geom-simu", help = "plot geometry and simulation", action="store_true")
    parser.add_argument("-sg", "--simu-geom", help = "plot simulation and geometry", action="store_true")

    parser.add_argument("-dgs", "--data-geom-simu", help = "plot data, geometry, and simulation", action="store_true")
    parser.add_argument("-dsg", "--data-simu-geom", help = "plot data, simulation, and geometry", action="store_true")
    parser.add_argument("-gds", "--geom-data-simu", help = "plot geometry, data, and simulation", action="store_true")
    parser.add_argument("-gsd", "--geom-simu-data", help = "plot geometry, simulation, and data", action="store_true")
    parser.add_argument("-sdg", "--simu-data-geom", help = "plot simulation, data, and geometry", action="store_true")
    parser.add_argument("-sgd", "--simu-geom-data", help = "plot simulation, geometry, and data", action="store_true")
    
    # Other arguments:
    
    parser.add_argument("-f", "--field", help = "electric field in V/cm", type = float, default = 1000.0)
    parser.add_argument("-e", "--events", help = "number of events", type = int, default = 1000000)
    parser.add_argument("-p", "--points", help = "number of points", type = int, default = 100)
    parser.add_argument("-min", "--min-energy", help = "minimum energy in MeV", type = float, default = 0.0)
    parser.add_argument("-max", "--max-energy", help = "maximum energy in MeV", type = float, default = 2.0)
    parser.add_argument("-dev", "--energy-std-dev", help = "energy standard deviation in MeV", type = float, default = 0.05)
    parser.add_argument("-scale", "--energy-scale", help = "energy scale", nargs = "*", type = float, default = [1.0])
    parser.add_argument("-a", "--atten-dist", help = "attenuation distance in mm", type = float, default = 1000.0)
    parser.add_argument("-if", "--input-files", help = "Input filenames", nargs = "*", type = str, default = [])

    return parser

####################################################################################################

def printArguments(args):
    """
    Print a formatted summary of the arguments.
    """
    print("╔" + "═"*62 + "╗")
    print("║" + " "*13 + f"puritymonitor command-line interface" + " "*13 + "║")
    print("║" + " "*13 + f"   released under the MIT License   " + " "*13 + "║")
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

def getFigures(nPurityMonitors: int, args):
    """
    """

    figs = {}
    
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