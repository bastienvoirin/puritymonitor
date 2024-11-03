import numpy as np
from typing import Self # For type hint only
from collections.abc import Iterable # For type hint only
from ..types import float_MeV # For type hint only

####################################################################################################

class EnergyBins:
    """
    Utility class allowing easy manipulation of energy discretization over a given range.
    """

    def __init__(
        self,
        lower: Iterable[float_MeV],
        upper: Iterable[float_MeV],
        nBins: int,
        binWidth: float_MeV
    ):
        self.lower = lower
        self.upper = upper
        self.nBins = nBins
        self.binWidth = binWidth

    def __str__(
        self
    ) -> str:
        """
        Readable representation of an `EnergyBins` instance.
        """
        return f"EnergyBins({self.lower[0]} to {self.upper[-1]}, {self.nBins} bins)"
    
    def __repr__(
        self
    ) -> str:
        """
        Unambiguous, explicit string representation of an `EnergyBins` instance.
        """
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
    ) -> bool:
        """
        Equality test between two `EnergyBin` instances, i.e. whether they describe the same energy
        discretization. In Python,

        ```
        energyBins1 == energyBins2
        ```

        calls

        ```
        energyBins1.__eq__(energyBins2)
        ```
        
        under the hood.
        """

        # Comparison between an `EnergyBins` instance and any other object is not implemented.
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        
        return (
                all(np.isclose(self.lower, other.lower, atol = 0.0, rtol = 1e-12)) # Relative tolerance
            and all(np.isclose(self.upper, other.upper, atol = 0.0, rtol = 1e-12)) # Relative tolerance
            and self.nBins == other.nBins
            and self.binWidth == other.binWidth
        )
    
    def scale(
        self,
        scale: float
    ) -> Self:
        """
        """
        for index, lower in enumerate(self.lower): self.lower[index] = lower * scale
        for index, upper in enumerate(self.upper): self.upper[index] = upper * scale
        self.binWidth *= scale
        return self
    
    @classmethod
    def fromRange(
        cls,
        minEnergy: float_MeV = 0.0,
        maxEnergy: float_MeV = 2.0,
        nBins: int = 100
    ):
        """
        Construct an `EnergyBins` instance from a minimum energy, a maximum energy, and a number of
        energy bins. Example:

        ```
        energyBins = EnergyBins.fromRange(minEnergy = 0.0, maxEnergy = 2.0, nBins = 100)
        ```
        """

        linSpace = np.linspace(start = minEnergy, stop = maxEnergy, num = nBins + 1, dtype = float)

        return EnergyBins(
            lower = linSpace[:-1].copy(),
            upper = linSpace[1:].copy(),
            nBins = nBins,
            binWidth = (maxEnergy - minEnergy) / nBins
        )
    
    @classmethod
    def fromLower(
        cls,
        lower: Iterable[float_MeV]
    ):
        """
        Construct an `EnergyBins` instance from the lower bounds of energy bins. Example:

        ```
        energyBins = EnergyBins.fromLower(np.linspace(0.0, 2.0, num = 100, endpoint = False))
        ```
        """

        return EnergyBins(
            lower = lower,
            upper = None, # To do
            nBins = len(lower),
            binWidth = None # To do
        )
    
    @classmethod
    def fromUpper(
        cls,
        upper: Iterable[float_MeV]
    ):
        """
        Construct an `EnergyBins` instance from the upper bounds of energy bins. Example:

        ```
        energyBins = EnergyBins.fromUpper(np.linspace(0.02, 2.0, num = 100))
        ```
        """

        return EnergyBins(
            lower = None, # To do
            upper = upper,
            nBins = len(upper),
            binWidth = None # To do
        )