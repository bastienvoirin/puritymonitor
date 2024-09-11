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
        description: str = "RadioactiveElectronSource"
    ) -> None:
        self.electrons = electrons
        self.gammas = gammas
        self.description = description
        
    def __str__(
        self
    ) -> str:
        return self.description
        
    def decay(
        self
    ):
        raise NotImplementedError
