from puritymonitor import (
    Bi207,
    CylinderConcentricTwoPartAnode as Cylinder,
    PurityMonitorInitDecay as PM,
    EnergySpectra
)

from matplotlib import pyplot as plt
import matplotlib as mpl

plt.rc("font", family = "serif", size = 10)
mpl.rc("text", usetex = True)
mpl.rc("legend", fontsize = 10)

if __name__ == "__main__":
    ###############################
    # Define a dual purity monitor:

    shortPM = PM(Bi207(), Cylinder(innerRadius = 15.0, outerRadius = 30.0, driftLength = 65.0))
    longPM = PM(Bi207(), Cylinder(innerRadius = 15.0, outerRadius = 30.0, driftLength = 185.0))

    #################################################################
    # Define params for both Monte Carlo simulations and experiments:

    params = {
        "nEvents": 10_000_000,
        "nBins": 100,
        #"energyStdDev": 0.035,
        "attDistance": 458.5,
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
        "differenceColor": "darkgray",
        "fittedPeaksColor": "black",
        "innerAnodeLabel": "Inner anode",
        "outerAnodeLabel": "Outer anode",
        "differenceLabel": "Difference",
        "fittedPeaksLabel": lambda means, stdDevs: f"IC peak fit:\n{means[0]:.3f}\\,V",
        #"fittedPeaksLabel": lambda means, stdDevs: f"IC peak fit {round(means[0]*1000):.0f}\\,mV",
    }

    ##############################
    # Run Monte Carlo simulations:

    shortScale = 1.0
    longScale = 1.0

    print("0/2")
    shortPM.simulateEnergySpectra(**params, energyStdDev = 0.067, energyScale = shortScale, minEnergy = 0.312/shortScale, maxEnergy = 1.4/shortScale)
    print("1/2")
    longPM.simulateEnergySpectra(**params, energyStdDev = 0.067, energyScale = longScale, minEnergy = 0.312/longScale, maxEnergy = 1.4/longScale)
    print("2/2")

    ####################################
    # Initialize figure(s) and subplots:

    fig, ((axShortSim, axLongSim), (axShortExp, axLongExp)) = plt.subplots(
        2, 2,
        figsize = (9, 6),
        layout = "constrained"
    )

    ##############################################################
    # Plot spectra and Gaussian fits from Monte Carlo simulations:

    shortPM.plotAnodeSpectra(axShortSim, energyStdDev = 0.067, manualScale = 0.94, **params, legendTitle = "Short purity monitor\nSimulation") # "\\textbf{Short purity monitor}\n\\textbf{Simulation}")
    longPM.plotAnodeSpectra(axLongSim, energyStdDev = 0.067, manualScale = 1.03, **params, legendTitle = "Long purity monitor\nSimulation") # "\\textbf{Long purity monitor}\n\\textbf{Simulation}")
    
    ##################################################
    # Plot spectra and Gaussian fits from experiments:

    for pm, axExp, energyStdDev, filename, manualScale, legendTitle in (
        (shortPM, axShortExp, 0.05, "./data/inner_outer_short_new.csv", 0.9, "Short"),
        #(longPM, axLongExp, 0.05, "./data/inner_outer_long_new.csv", 1.0, "Long")
    ):
        data = EnergySpectra.load(filename = filename)
        pm.plotAnodeSpectra(
            axExp,
            energyScale = 0.5,
            energyStdDev = energyStdDev,
            **params,
            energyBins = data.energyBins,
            innerAnodeSpectrum = data.spectra[0],
            outerAnodeSpectrum = data.spectra[1],
            nPeaks = 2,
            manualScale = manualScale,
            legendTitle = f"{legendTitle} purity monitor\nExperiment" # "\\textbf{??? purity monitor}\n\\textbf{Experiment}")
        )

    ##############################
    # Show and save the figure(s):

    plt.savefig("./static/jinst_dual_pm_sim_exp_10M_new.svg")
    plt.savefig("./static/jinst_dual_pm_sim_exp_10M_new.png", dpi = 300)
    plt.show()