from . import RadioactiveSource
from ..types import float_MeV, float_mm, float_kBq

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
        electronEnergy: list[float_MeV] = [0.4817, 0.55575, 0.5665, 0.8098, 0.9757, 1.049, 1.060, 1.682],
        gammaEnergy: list[float_MeV] = [0.32812, 0.5110, 0.569702, 0.8978, 1.063662, 1.4422, 1.770237],
        electronProba: list[float] = [0.0152, 0.0044, 0.0015, 0.0, 0.0703, 0.0184, 0.0054, 0.0], # To do
        gammaProba: list[float] = [0.0, 0.0, 0.980, 0.0, 0.750, 0.0, 0.069], # To do
        gammaComptonDistance: list[float_mm] = [0.0, 0.0, 80.0, 0.0, 120.0, 0.0, 160.0], # To do
        activity: float_kBq = float("NaN"),
        description: str = "Bi-207 radioactive source"
    ) -> None:
        super().__init__(
            electronEnergy = electronEnergy,
            gammaEnergy = gammaEnergy,
            electronProba = electronProba,
            gammaProba = gammaProba,
            gammaComptonDistance = gammaComptonDistance,
            activity = activity,
            description = description
        )
