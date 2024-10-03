from matplotlib import pyplot as plt
from puritymonitor import (
    Bi207,
    CylinderConcentricTwoPartAnode as Cylinder,
    PurityMonitorInitDecay as PM
)

if __name__ == "__main__":
    # Dual purity monitor definition:

    shortPM = PM(Bi207(), Cylinder(innerRadius = 15.0, outerRadius = 30.0, driftLength = 65.0))
    longPM = PM(Bi207(), Cylinder(innerRadius = 15.0, outerRadius = 30.0, driftLength = 185.0))

    # Dual purity monitor TPC geometry visualization:

    fig, (axS, axL) = plt.subplots(1, 2, subplot_kw = {"projection": "3d"})
    shortPM.draw(axS)
    longPM.draw(axL)

    # Monte Carlo simulation:

    simulation = {
        "nEvents": 1000000,
        "nBins": 100,
        "minEnergy": 0.2,
        "maxEnergy": 1.7,
        "energyScale": 1.0,
        "energyStdDev": 0.025,
        "attDistance": 1000.0
    }

    fig, (axS, axL) = plt.subplots(1, 2, figsize = (12, 4))
    shortPM.energySpectra(**simulation)
    longPM.energySpectra(**simulation)
    shortPM.plotAnodeSpectra(axS)
    longPM.plotAnodeSpectra(axL)
    fig.tight_layout()

    plt.show()