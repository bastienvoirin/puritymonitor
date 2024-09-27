import numpy as np
from collections.abc import Generator # For type hint only

################################################################################

class RadioactiveElectronSource:
    """
    Abstract base class to inherit from and implement.
    """
    def __init__(
        self,
        electronEnergy: list = [],
        gammaEnergy: list = [],
        electronProba: list = [],
        gammaProba: list = [],
        activity: float = float("NaN"),
        description: str = "Unspecified radioactive electron source"
    ) -> None:
        assert len(electronEnergy) == len(electronProba)
        assert len(gammaEnergy) == len(gammaProba)

        self.electronEnergy = electronEnergy
        self.gammaEnergy = gammaEnergy
        self.electronProba = electronProba
        self.gammaProba = gammaProba
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
        
    def __str__(
        self
    ) -> str:
        return self.description
        
    def __repr__(
        self
    ) -> str:
        return "\n".join([
            f"RadioactiveElectronSource(",
            f"  electronEnergy = {self.electronEnergy}",
            f"  gammaEnergy = {self.gammaEnergy}",
            f"  electronProba = {self.electronProba}",
            f"  gammaProba = {self.gammaProba}",
            f"  activity = {self.activity}",
            f"  description = {self.description}",
            f")"
        ])
    
    def decay(
        self,
        nEvents = 1000000
    ) -> Generator[tuple, None, None]:
        """
        Generator of decay products of Bi-207.
        """
        for _ in range(nEvents):
            energy, isElectron = np.random.choice(
                zip(self.energy, self.isElectron),
                p = self.proba
            )
            yield energy, isElectron

    def fullDecay(
        self,
        events = 1000000
    ) -> Generator[tuple, None, None]:
        """
        Generator of decay products starting from an initial Bi-207 atom up to a
        ground state Pb-207 nucleus.
        """
        raise NotImplementedError
