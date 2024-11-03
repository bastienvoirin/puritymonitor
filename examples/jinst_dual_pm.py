#!/usr/bin/python3

from puritymonitor import (
    Bi207,
    CylinderConcentricTwoPartAnode as Cylinder,
    PurityMonitorInitDecay as PM
)

from matplotlib import pyplot as plt
import matplotlib as mpl

plt.rc("font", family = "serif", size = 10)
mpl.rc("text", usetex = True)
mpl.rc("legend", fontsize = 10)

if __name__ == "__main__":
    # Dual purity monitor definition:

    shortPM = PM(Bi207(), Cylinder(innerRadius = 15.0, outerRadius = 30.0, driftLength = 65.0))
    longPM = PM(Bi207(), Cylinder(innerRadius = 15.0, outerRadius = 30.0, driftLength = 185.0))

    # Monte Carlo simulation:

    simulation = {
        "nEvents": 10_000_000,
        "nBins": 105,
        "energyStdDev": 0.035,
        "attDistance": 500.0,
        "xAxisLabel": "Pulse height (V)",
        "yAxisLabel": "Counts",
        "frameColor": "blue",
        "gridParams": {
            "color": "blue",
            "linestyle": "dotted",
            "alpha": 0.5
        },
        "innerAnodeColor": "tab:cyan",
        "outerAnodeColor": "tab:orange",
        "differenceColor": "tab:brown",
        "fittedPeaksColor": "tab:green",
        "innerAnodeLabel": "Inner anode",
        "outerAnodeLabel": "Outer anode",
        "differenceLabel": "Weighted difference",
        "fittedPeaksLabel": lambda means, stdDevs: f"IC peak fit {means[0]:.3f}\\,V",
        #"fittedPeaksLabel": lambda means, stdDevs: f"IC peak fit {round(means[0]*1000):.0f}\\,mV",
    }

    shortPM.energySpectra(**simulation, energyScale = 0.82, minEnergy = 0.2/0.82, maxEnergy = 1.25/0.82)
    longPM.energySpectra(**simulation, energyScale = 0.75, minEnergy = 0.2/0.75, maxEnergy = 1.25/0.75)

    fig, (axS, axL) = plt.subplots(1, 2, figsize = (9, 3), layout = "constrained")
    shortPM.plotAnodeSpectra(axS, **simulation, legendTitle = "Short purity monitor\nSimulation") # "\\textbf{Short purity monitor}\n\\textbf{Simulation}")
    longPM.plotAnodeSpectra(axL, **simulation, legendTitle = "Long purity monitor\nSimulation") # "\\textbf{Long purity monitor}\n\\textbf{Simulation}")

    # TODO: plot experiment data

    plt.savefig("static/jinst_dual_pm.svg")
    plt.savefig("static/jinst_dual_pm.png", dpi = 300)
    plt.show()