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

    def __str__(
        self
    ):
        return f"EnergyBins({self.lower[0]} to {self.upper[-1]}, {self.nBins} bins)"
    
    def __repr__(
        self
    ):
        return "\n".join([
            "EnergyBins(",
            f"  lower = {repr(self.lower)},",
            f"  upper = {repr(self.upper)},",
            f"  nBins = {repr(self.nBins)},",
            f"  binWidth = {repr(self.binWidth)}",
            ")"
        ])
    
    def __eq__(
        self,
        other
    ):
        """
        """
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        return (
                all(np.isclose(self.lower, other.lower, atol = 0.0, rtol= 1e-12))
            and all(np.isclose(self.upper, other.upper, atol = 0.0, rtol= 1e-12))
            and self.nBins == other.nBins
            and self.binWidth == other.binWidth
        )
    
    def fromRange(
        self,
        minEnergy: float = 0.0,
        maxEnergy: float = 2.0,
        nBins: int = 100
    ):
        """
        """
        linSpace = np.linspace(start = minEnergy, stop = maxEnergy, num = nBins + 1, dtype = float)
        self.lower = linSpace[:-1]
        self.upper = linSpace[1:]
        self.nBins = nBins
        self.binWidth = (maxEnergy - minEnergy) / nBins
        return self