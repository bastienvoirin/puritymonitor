import numpy as np
from collections.abc import Generator # For type hint only
from ..types import float_MeV, float_mm, float_kBq

####################################################################################################

class RadioactiveSource:
    """
    Abstract base class to inherit from and implement.
    """
    def __init__(
        self,
        electronEnergy: list[float_MeV] = [],
        gammaEnergy: list[float_MeV] = [],
        electronProba: list[float] = [],
        gammaProba: list[float] = [],
        gammaComptonDistance: list[float_mm] = [],
        activity: float_kBq = float("NaN"),
        description: str = "unspecified radioactive source"
    ) -> None:
        assert len(electronEnergy) == len(electronProba)
        assert len(gammaEnergy) == len(gammaProba) == len(gammaComptonDistance)

        self.electronEnergy = electronEnergy
        self.gammaEnergy = gammaEnergy
        self.electronProba = electronProba
        self.gammaProba = gammaProba
        self.gammaComptonDistance = gammaComptonDistance
        self.activity = activity
        self.description = description

        # Concatenate electrons and gamma photons
        self.energy = np.array([*self.electronEnergy, *self.gammaEnergy])
        self.proba = np.array([*self.electronProba, *self.gammaProba])
        self.proba /= np.sum(self.proba)

        # Boolean mask
        self.isElectron = np.concatenate((
            np.ones(len(self.electronEnergy), dtype = bool),
            np.zeros(len(self.electronEnergy), dtype = bool)
        ))

        # Distance between the decay vertex and the electron emission vertex
        self.electronEmissionDistance = np.concatenate((
            np.zeros(len(self.electronEnergy), dtype = float),
            np.array(self.gammaComptonDistance, dtype = float)
        ))
        
    def __str__(
        self
    ) -> str:
        return self.description
        
    def __repr__(
        self
    ) -> str:
        return "\n".join([
            f"{self.__class__.__name__}(",
            f"  electronEnergy = {repr(self.electronEnergy)},",
            f"  gammaEnergy = {repr(self.gammaEnergy)},",
            f"  electronProba = {repr(self.electronProba)},",
            f"  gammaProba = {repr(self.gammaProba)},",
            f"  gammaComptonDistance = {repr(self.gammaComptonDistance)},",
            f"  activity = {repr(self.activity)},",
            f"  description = {repr(self.description)}",
            ")"
        ]).replace("nan", "float('NaN')")
    
    def __eq__(
        self,
        other
    ):
        """
        Equality test between two `RadioactiveSource` instances, i.e. whether they describe the same
        radioactive source. In Python,

        ```
        radioactiveSource1 == radioactiveSource2
        ```

        calls

        ```
        radioactiveSource1.__eq__(radioactiveSource2)
        ```
        
        under the hood.
        """

        # Comparison between a `RadioactiveSource` instance and any other object is not implemented.
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        
        return (
                self.electronEnergy == other.electronEnergy
            and self.gammaEnergy == other.gammaEnergy
            and self.electronProba == other.electronProba
            and self.gammaProba == other.gammaProba
            and self.gammaComptonDistance == other.gammaComptonDistance
            and ((self.activity == other.activity) or (np.isnan(self.activity) and np.isnan(other.activity)))
            and self.description == self.description
        )
    
    def decay(
        self,
        nEvents = 1000000
    ) -> Generator[tuple[any, bool, float], None, None]:
        """
        Generator of possible initial decay products of a parent radioactive isotope.
        """

        zipped = tuple(zip(self.energy, self.isElectron, self.electronEmissionDistance))

        for _ in range(nEvents):
            yield zipped[np.random.choice(len(zipped), p = self.proba)]
