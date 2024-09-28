from . import RadioactiveSource

####################################################################################################

class Bi207(RadioactiveSource):
    """
    Bi-207 radioactive source, which decays almost exclusively by electron capture (EC) to an
    excited Pb-207 nucleus with a vacant inner (mostly K, sometimes L) electron orbital.

    High-energy (100 keV to 2 MeV) decay products:
    - internal conversion (IC) electrons;
    - gamma photons.

    Low-energy (0 to 100 keV) decay products:
    - Auger electrons;
    - X-rays.
    """
    def __init__(
        self,
        electronEnergy: list = [481.7, 555.75, 566.5, 809.8, 975.7, 1049.0, 1060.0, 1682.0],
        gammaEnergy: list = [328.12, 511.0, 569.702, 897.8, 1063.662, 1442.2, 1770.237],
        electronProba: list = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], # To do
        gammaProba: list = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], # To do
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
