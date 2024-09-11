from . import RadioactiveElectronSource

####################################################################################################

class Bi207InLAr(RadioactiveElectronSource):
    """
    Bi-207 (electron capture) radioactive electron source in liquid argon (LAr).
    """
    def __init__(
        self,
        electronEnergy: list = [],
        gammaEnergy: list = [],
        electronProba: list = [],
        gammaProba: list = [],
        activity: float = float("NaN")
    ) -> None:
        super().__init__(
            electronEnergy = electronEnergy,
            gammaEnergy = gammaEnergy,
            electronProba = electronProba,
            gammaProba = gammaProba,
            activity = activity,
            description = "Bi-207 in LAr"
        )
        
    def decay(
        self
    ):
        """
        Generator of decay products starting from an initial Bi-207 atom up to a ground state Pb-207
        nucleus.
        """
        yield
