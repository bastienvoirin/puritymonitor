from .. import RadioactiveSource
from .. import Geometry
import numpy as np

####################################################################################################

class PurityMonitor:
    def __init__(
        self,
        radioactiveSource: RadioactiveSource,
        geometry: Geometry
    ) -> None:
        self.radioactiveSource = radioactiveSource
        self.geometry = geometry
        
    def __str__(
        self
    ) -> str:
        return " ".join([
            "{self.radioactiveSource} LAr purity monitor\n"
        ])
        
    def draw(
        self,
        ax
    ) -> None:
        self.geometry.draw(ax)

    def energySpectra(
        self,
        nEvents: int = 1000000,     # Number of events to simulate
        nPoints: int = 200,         # Number of energy bins
        minEnergy: float = 0.0,     # Lowest energy in arbitrary units
        maxEnergy: float = 2.0,     # Highest energy in arbitrary units
        energyScale: float = 1.0,   # Arbitrary units per MeV
        energyStdDev: float = 0.1,  # Electron energy standard deviation
        attDistance: float = 1000.0 # Electron attenuation distance in mm
    ):
        """
        """

        for energy, isElec, elecEmissionDist in self.radioactiveSource.initDecay(nEvents = nEvents):
            emissionVertex, emissionDirection = self.geometry.emissionVertexAndDirection()

            # Sample a random propagation distance `propDist` before Compton electron emission from
            # an exponential probability density function of characteristic distance `propDist0`
            propDist = -elecEmissionDist * np.log(np.random.random())

            self.geometry.isInsideActiveVolume()
        
        return energies, (innerAnodeSpectrum, outerAnodeSpectrum)
