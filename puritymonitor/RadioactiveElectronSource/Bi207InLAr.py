from . import RadioactiveElectronSource

####################################################################################################

class Bi207InLAr(RadioactiveElectronSource):
    """
    Bi-207 radioactive electron source (internal conversion electrons induced by electron capture)
    in liquid argon (LAr).
    """
    def __init__(
        self,
        electronEnergy: list = [],
        gammaEnergy: list = [],
        electronProba: list = [],
        gammaProba: list = [],
        activity: float = float("NaN"),
        description: str = "Bi-207 radioactive electron source in LAr"
    ) -> None:
        super().__init__(
            electronEnergy = electronEnergy,
            gammaEnergy = gammaEnergy,
            electronProba = electronProba,
            gammaProba = gammaProba,
            activity = activity,
            description = description
        )
