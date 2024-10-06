from matplotlib import pyplot as plt
import matplotlib as mpl
plt.rc("font", family = "serif", size = 11)
mpl.rc("text", usetex = True)
mpl.rc("legend", fontsize = 11)

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
        "minEnergy": 0.0,
        "maxEnergy": 2.0,
        "energyScale": 1.0,
        "energyStdDev": 0.05,
        "attDistance": 1000.0
    }

    fig, (axS, axL) = plt.subplots(1, 2, figsize = (9, 3), layout = "constrained")
    shortPM.energySpectra(**simulation)
    longPM.energySpectra(**simulation)
    shortPM.plotAnodeSpectra(axS, **simulation)
    longPM.plotAnodeSpectra(axL, **simulation)

    plt.show()