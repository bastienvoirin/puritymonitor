from numpy import array
from puritymonitor import (
    Bi207,
    CylinderConcentricTwoPartAnode,
    EnergyBins, # Needed to assert eval(repr(energyBins)) == energyBins
    PurityMonitorInitDecay
)

if __name__ == "__main__":
    # Dual purity monitor definition:

    source = Bi207()
    print(source)
    print()
    print(repr(source))
    assert eval(repr(source)) == source

    print()

    geometry = CylinderConcentricTwoPartAnode(innerRadius = 15.0, outerRadius = 30.0, driftLength = 60.0)
    print(geometry)
    print()
    print(repr(geometry))
    assert eval(repr(geometry)) == geometry

    print()

    monitor = PurityMonitorInitDecay(source, geometry)
    print(monitor)
    print()
    print(repr(monitor))
    assert eval(repr(monitor)) == monitor

    # Monte Carlo simulation:

    simulation = {
        "nEvents": 1000,
        "nBins": 100,
        "minEnergy": 0.0,
        "maxEnergy": 2.0,
        "energyScale": 1.0,
        "energyStdDev": 0.05,
        "attDistance": 1000.0
    }

    print()

    energyBins, energySpectra = monitor.energySpectra(**simulation)

    print(energyBins)
    print()
    print(repr(energyBins))
    assert eval(repr(energyBins)) == energyBins

    print()

    print(*energySpectra, sep = "\n")
    print()
    print(*map(repr, energySpectra), sep = "\n")