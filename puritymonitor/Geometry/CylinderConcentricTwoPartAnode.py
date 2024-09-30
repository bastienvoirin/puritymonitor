from ..EnergySpectra import EnergyBins
from .Geometry import Geometry, cylinder, ring
import numpy as np

####################################################################################################

class CylinderConcentricTwoPartAnode(Geometry):
    """
    Cylindrical TPC geometry with concentric inner disk anode and outer ring anode.
    """
    def __init__(
        self,
        innerRadius: float,
        outerRadius: float,
        driftLength: float
    ):
        self.description = "CylinderConcentricTwoPartAnode"
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.driftLength = driftLength
        self.energyBins = EnergyBins()
        self.innerAnodeSpectrum = []
        self.outerAnodeSpectrum = []
        
    def draw(
        self,
        ax
    ):
        """
        Draw the geometry.
        """
        ax.plot_surface(
            *cylinder(radius = self.outerRadius, height = self.driftLength),
            alpha = 0.125,
            color = "k",
            shade = False
        )
        ax.plot_surface(
            *ring(innerRadius = 0, outerRadius = self.innerRadius, planeZ = self.driftLength),
            alpha = 0.5,
            color = "tab:blue",
            shade = False
        )
        ax.plot_surface(
            *ring(innerRadius = self.innerRadius, outerRadius = self.outerRadius, planeZ = self.driftLength),
            alpha = 0.5,
            color = "tab:orange",
            shade = False
        )
        ax.plot_surface(
            *ring(innerRadius = 0, outerRadius = self.outerRadius, planeZ = 0),
            alpha = 0.25,
            color = "k",
            shade = False
        )
        ax.plot(
            [0], [0], [0],
            alpha = 1.,
            markerfacecolor = "tab:green",
            markeredgecolor = "tab:green",
            marker = "o"
        )
        
        # Equal axes (https://github.com/matplotlib/matplotlib/issues/17172#issuecomment-830139107)
        ax.set_box_aspect([
            upperBound - lowerBound
            for lowerBound, upperBound in (getattr(ax, f"get_{axis}lim")() for axis in "xyz")
        ])
        
    def isInsideActiveVolume(
        self,
        x: float,
        y: float,
        z: float
    ) -> bool:
        """
        Indicate whether a given 3D point (x, y, z) lies inside the active volume.
        """
        return ((x**2 + y**2) <= self.outerRadius**2) and (0 <= z <= self.driftLength)
    
    def decayVertexAndDirection(
        self
    ) -> tuple[tuple[float, float, float], tuple[float, float]]:
        """
        Sample a random IC electron or gamma emission vertex at the surface of the radioactive
        source, and a random direction in the upper half-space (i.e. from the cathode plane to the
        anode plane).
        """
        x = 0.0 # To do
        y = 0.0 # To do
        z = 0.0 # To do
        theta = np.pi * np.random.random()
        phi = 2 * np.pi * np.random.random()
        return (x, y, z), (theta, phi)
    
    def resetAnodeSpectra(
        self,
        nBins: int = 100,
        minEnergy: float = 0.0,
        maxEnergy: float = 2.0,
        energyScale: float = 1.0
    ):
        self.innerAnodeSpectrum = np.zeros(nBins, dtype = int)
        self.outerAnodeSpectrum = np.zeros(nBins, dtype = int)
        self.energyBins = EnergyBins().fromRange(
            minEnergy = minEnergy,
            maxEnergy = maxEnergy,
            nBins = nBins
        )
    
    def updateAnodeSpectra(
        self,
        x: float,
        y: float,
        z: float,
        energy: float
    ):
        mask = (energy > self.energyBins.lower) & (energy < self.energyBins.upper)
        if 0 <= z <= self.driftLength:
            if (x**2 + y**2) <= self.innerRadius**2:
                self.innerAnodeSpectrum[mask] += 1 # To do: increment event count for the right energy bin
            elif (x**2 + y**2) <= self.outerRadius**2:
                self.outerAnodeSpectrum[mask] += 1 # To do: increment event count for the right energy bin
    
    def getAnodeSpectra(
        self
    ):
        return self.innerAnodeSpectrum, self.outerAnodeSpectrum
    
    def plotAnodeSpectra(
        self,
        ax,
        innerAnodeColor: str = "tab:blue",
        outerAnodeColor: str = "tab:orange",
        swapAnodes: bool = False
    ):
        ax.set_xlabel("Energy (MeV)")

        ax.set_ylabel("Inner anode", color = innerAnodeColor)
        ax.plot(self.energyBins.lower, self.innerAnodeSpectrum, color = innerAnodeColor) # To do: plot
        ax.tick_params(axis = "y", labelcolor = innerAnodeColor)

        ax = ax.twinx() # Instantiate a second `Axes` object that shares the same x-axis

        ax.set_ylabel("Outer anode", color = outerAnodeColor)
        ax.plot(self.energyBins.lower, self.outerAnodeSpectrum, color = outerAnodeColor) # To do: plot
        ax.tick_params(axis = "y", labelcolor = outerAnodeColor)