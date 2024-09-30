from .. import RadioactiveSource
from .. import Geometry
from .. import EnergyBins
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
        nBins: int = 100,           # Number of energy bins
        minEnergy: float = 0.0,     # Lowest energy in arbitrary units
        maxEnergy: float = 2.0,     # Highest energy in arbitrary units
        energyScale: float = 1.0,   # Arbitrary units per MeV
        energyStdDev: float = 0.0,  # Electron energy standard deviation/resolution/systematic error
        attDistance: float = 1000.0 # Electron attenuation distance in mm
    ):
        """
        """
        self.geometry.resetAnodeSpectra(
            nBins = nBins,
            minEnergy = minEnergy,
            maxEnergy = maxEnergy,
            energyScale = energyScale
        )

        for energy, isElec, elecDist in self.radioactiveSource.decay(nEvents = nEvents):
            (x0, y0, z0), (theta, phi) = self.geometry.decayVertexAndDirection()

            # Sample a random propagation distance `propDist` before Compton electron emission from
            # an exponential probability density function of characteristic distance `elecDist`
            propDist = -elecDist * np.log(np.random.random())

            # Random electron emission vertex
            # (which might be outside of the active volume for Compton electrons)
            x1 = x0 + propDist * np.sin(theta) * np.sin(phi)
            y1 = y0 + propDist * np.sin(theta) * np.cos(phi)
            z1 = z0 + propDist * np.cos(theta)

            # Discard events for which the electron emission vertex lies outside of the LAr volume
            if not self.geometry.isInsideActiveVolume(x1, y1, z1):
                continue

            # To do: process electron if it is an electron
            # To do: process gamma if it is a gamma photon

            if energy >= 0:
                energy *= np.exp(-(self.geometry.driftLength - z1) / attDistance)
                
                # Electron energy resolution/systematic error
                energy += np.random.normal(loc = 0.0, scale = energyStdDev)

                # Increment the event count for right anode
                self.geometry.updateAnodeSpectra(x1, y1, z1, energy / 1000)
        
        return self.geometry.energyBins, self.geometry.anodeSpectra
    
    def plotAnodeSpectra(
        self,
        ax,
        **kwargs
    ):
        return self.geometry.plotAnodeSpectra(ax = ax, **kwargs)
