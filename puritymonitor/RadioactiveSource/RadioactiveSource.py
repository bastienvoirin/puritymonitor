import numpy as np
from collections.abc import Generator # For type hint only

####################################################################################################

class RadioactiveSource:
    """
    Abstract base class to inherit from and implement.
    """
    def __init__(
        self,
        electronEnergy: list = [],
        gammaEnergy: list = [],
        electronProba: list = [],
        gammaProba: list = [],
        gammaComptonDistance: list = [],
        activity: float = float("NaN"),
        description: str = "Unspecified radioactive source"
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
            f"RadioactiveSource(",
            f"  electronEnergy = {self.electronEnergy}",
            f"  gammaEnergy = {self.gammaEnergy}",
            f"  electronProba = {self.electronProba}",
            f"  gammaProba = {self.gammaProba}",
            f"  gammaComptonDistance = {self.gammaComptonDistance}",
            f"  activity = {self.activity}",
            f"  description = {self.description}",
            f")"
        ])
    
    def decay(
        self,
        nEvents = 1000000
    ) -> Generator[tuple, None, None]:
        """
        Generator of possible initial decay products of a parent radioactive isotope.
        """
        zipped = tuple(zip(self.energy, self.isElectron, self.electronEmissionDistance))
        for _ in range(nEvents):
            yield zipped[np.random.choice(len(zipped), p = self.proba)]
