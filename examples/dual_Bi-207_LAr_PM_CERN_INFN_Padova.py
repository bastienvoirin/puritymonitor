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

    fig, (axS, axL) = plt.subplots(2)
    shortPM.draw(axS)
    longPM.draw(axL)

    fig, (axS, axL) = plt.subplots(2)
    # To do: simulation
    # To do: simulation