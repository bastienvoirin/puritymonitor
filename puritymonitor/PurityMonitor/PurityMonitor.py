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
        """
        """
        return f"purity monitor ({self.radioactiveSource}, {self.geometry})"
    
    def __repr__(
        self
    ) -> str:
        """
        """
        return "\n".join([
            f"{self.__class__.__name__}(",
            "\n".join(map(lambda line: f"  {line}", repr(self.radioactiveSource).split("\n"))) + ",",
            "\n".join(map(lambda line: f"  {line}", repr(self.geometry).split("\n"))),
            ")"
        ])
    
    def __eq__(
        self,
        other
    ):
        """
        """
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        return (self.radioactiveSource == other.radioactiveSource) and (self.geometry == other.geometry)
        
    def draw(
        self,
        ax
    ) -> None:
        """
        """
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
            maxEnergy = maxEnergy
        )

        for energy, isElec, elecDist in self.radioactiveSource.decay(nEvents = nEvents):
            (x0, y0, z0), (ctheta, stheta, phi) = self.geometry.decayVertexAndDirection()

            # Sample a random propagation distance `propDist` before Compton electron emission from
            # an exponential probability density function of characteristic distance `elecDist`
            propDist = -elecDist * np.log(np.random.random())
            
            # Random electron emission vertex
            # (which might be outside of the active volume for Compton electrons)
            x1 = x0 + propDist * stheta * np.sin(phi)
            y1 = y0 + propDist * stheta * np.cos(phi)
            z1 = z0 + propDist * ctheta

            # Discard events for which the electron emission vertex lies outside of the LAr volume
            if not self.geometry.isInsideActiveVolume(x1, y1, z1):
                continue

            # Electron
            if isElec:
                # Account for the foil on top of the Bi-207 radioactive source
                energyElec = max(0.0, energy - 0.0035 / ctheta)
            # Gamma photon
            else:
                success = False
                while not success:
                    ct = 2. * np.random.random() - 1. # Random value between -1 and +1
                    epsilon = 1. / (1. + energy / 0.511 * (1.0 - ct))
                    scatteringProba = 0.5 * epsilon**2 * (epsilon + 1 / epsilon - (1.0 - ct**2))
                    if np.random.random() <= scatteringProba:
                        success = True
                        energyGamma = energy * epsilon
                        energyElec = energy - energyGamma

            # Electron: account for the rim around the Bi-207 radioactive source
            if isElec:
                if ctheta <= 0.2:
                    energyElec *= ctheta/0.2

            if energyElec >= 0:
                #print(self.geometry.driftLength, z1, attDistance)
                energyElec *= np.exp(-(self.geometry.driftLength - z1) / attDistance)
                
                # Electron energy resolution/systematic error
                energyElec += np.random.normal(loc = 0.0, scale = energyStdDev)

                # Increment the event count for right anode
                self.geometry.updateAnodeSpectra(x1, y1, z1, energyElec)
        
        return self.geometry.energyBins, self.geometry.anodeSpectra
    
    def plotAnodeSpectra(
        self,
        ax,
        **kwargs
    ):
        """
        A wrapper for `self.geometry.plotAnodeSpectra(ax = ax, **kwargs)`.
        """
        return self.geometry.plotAnodeSpectra(ax = ax, **kwargs)
