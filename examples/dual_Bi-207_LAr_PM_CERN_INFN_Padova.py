from puritymonitor import (Bi207, CylinderConcentricTwoPartAnode, PurityMonitorInitDecay)
from matplotlib import pyplot as plt

if __name__ == "__main__":
    shortPM = PurityMonitorInitDecay(
        Bi207(),
        CylinderConcentricTwoPartAnode(innerRadius = 1.5, outerRadius = 3.0, driftLength = 6.5)
    )

    longPM = PurityMonitorInitDecay(
        Bi207(),
        CylinderConcentricTwoPartAnode(innerRadius = 1.5, outerRadius = 3.0, driftLength = 18.5)
    )

    #############################################
    # Purity monitor TPC geometry visualization #
    #############################################

    fig, (axS, axL) = plt.subplots(2)
    shortPM.draw(axS)
    longPM.draw(axL)

    ##########################
    # Monte Carlo simulation #
    ##########################

    simulation = {
        "nEvents": 1000000,
        "nBins": 100,
        "minEnergy": 0.0,
        "maxEnergy": 2.0,
        "energyScale": 1.0,
        "energyStdDev": 0.0,
        "attDistance": 1000.0
    }

    fig, (axS, axL) = plt.subplots(2)
    shortPM.energySpectra(**simulation)
    longPM.energySpectra(**simulation)
    shortPM.plotAnodeSpectra(axS)
    longPM.plotAnodeSpectra(axL)