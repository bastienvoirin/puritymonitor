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

        # Boolean mask
        self.isElectron = np.concatenate((
            np.ones(self.electronEnergy, dtype = bool),
            np.zeros(self.electronEnergy, dtype = bool)
        ))

        # Distance between the decay vertex and the electron emission vertex
        self.electronEmissionDistance = np.concatenate((
            np.zeros(self.electronEnergy, dtype = float),
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
    
    def initDecay(
        self,
        nEvents = 1000000
    ) -> Generator[tuple, None, None]:
        """
        Generator of possible initial decay products of a parent radioactive isotope.
        """
        for _ in range(nEvents):
            energy, isElectron, electronEmissionDistance = np.random.choice(
                zip(self.energy, self.isElectron, self.electronEmissionDistance),
                p = self.proba
            )
            yield energy, isElectron, electronEmissionDistance

    def fullDecay(
        self,
        events = 1000000
    ) -> Generator[tuple, None, None]:
        """
        Generator of decay products starting from a parent radioactive isotope to a ground-state
        child isotope.
        """
        raise NotImplementedError
