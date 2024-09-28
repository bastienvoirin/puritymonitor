import argparse
from . import printArgs, getFigs, getSubplots

####################################################################################################

def createParser():
    """
    Create an argument parser for the CLI command.
    """
    parser = argparse.ArgumentParser()
    
    # Figures to produce
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
    
    # Other arguments
    parser.add_argument("-f", "--field", help = "electric field in V/cm", type = float, default = 1000.0)
    parser.add_argument("-e", "--events", help = "number of events", type = int, default = 1000000)
    parser.add_argument("-p", "--points", help = "number of points", type = int, default = 100)
    parser.add_argument("-min", "--min-energy", help = "minimum energy in MeV", type = float, default = 0.0)
    parser.add_argument("-max", "--max-energy", help = "maximum energy in MeV", type = float, default = 2.0)
    parser.add_argument("-dev", "--energy-std-dev", help = "energy standard deviation in MeV", type = float, default = 0.05)
    parser.add_argument("-scale", "--energy-scale", help = "energy scale", nargs = "*", type = float, default = [1.0])
    parser.add_argument("-a", "--atten-dist", help = "attenuation distance in cm", type = float, default = 100.0)
    parser.add_argument("-ir", "--inner-radius", help = "inner radius in cm", type = float, default = 2.5)
    parser.add_argument("-or", "--outer-radius", help = "outer radius in cm", type = float, default = 5.0)
    parser.add_argument("-l", "--length", help = "PM TPC cathode-to-anode drift length(s) in cm", nargs = "*", type = float, default = "20.0")
    parser.add_argument("-r", "--relative-scale", help = "Outer anode to inner anode relative scaling factor", nargs = "*", type = float, default = "1.0")
    parser.add_argument("-if", "--input-files", help = "Input filenames", nargs = "*", type = str, default = [])

    return parser

####################################################################################################

def main(args):
    # To do
    subplots = getSubplots(*getFigs(nPurityMonitors, args))
    # To do
    return

####################################################################################################

if __name__ == "__main__":
    parser = createParser()
    args = parser.parse_args()
    printArgs(args)
    main(args)