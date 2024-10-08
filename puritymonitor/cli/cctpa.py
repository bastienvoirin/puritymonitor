"""
CLI command for the CylinderConcentricTwoPartAnode geometry.
"""

####################################################################################################

from argparse import ArgumentParser
from .main import createParser, printArguments, getFigures, getSubplots

####################################################################################################

def addArguments(parser: ArgumentParser):
    """
    Add CLI arguments specifically for the `python -m puritymonitor.cctpa` command.
    """
    
    parser.add_argument("-ir", "--inner-radius", help = "inner radius in mm", type = float, default = 25.0)
    parser.add_argument("-or", "--outer-radius", help = "outer radius in mm", type = float, default = 50.0)
    parser.add_argument("-l", "--length", help = "PM TPC drift length(s) in mm", nargs = "*", type = float, default = "200.0")

####################################################################################################

def main(arguments):

    # To do

    print(arguments)
    #subplots = getSubplots(*getFigures(1, arguments))

    # To do
    
    return

####################################################################################################

if __name__ == "__main__":
    parser = createParser()
    addArguments(parser)
    arguments = parser.parse_args()
    printArguments("python -m puritymonitor.cli.cctpa", arguments)
    main(arguments)