import numpy as np

####################################################################################################

class EnergyBins:
    def __init__(
        self,
        lower = None,
        upper = None,
        nBins: int = None,
        binWidth: float = None
    ):
        self.lower = lower
        self.upper = upper
        self.nBins = nBins
        self.binWidth = binWidth

    def fromRange(
        self,
        minEnergy: float = 0.0,
        maxEnergy: float = 2.0,
        nBins: int = 100
    ):
        linSpace = np.linspace(start = minEnergy, stop = maxEnergy, num = nBins + 1, dtype = float)
        self.lower = linSpace[:-1]
        self.upper = linSpace[1:]
        self.nBins = nBins
        self.binWidth = (maxEnergy - minEnergy) / nBins