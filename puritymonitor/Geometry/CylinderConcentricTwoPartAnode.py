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
        innerRadius: float, # mm
        outerRadius: float, # mm
        driftLength: float  # mm
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

        # Random point (x, y, z = 0) inside a disk of radius squared r² = 6.25
        while True:
            x = 5.0 * np.random.random() - 2.5
            y = 5.0 * np.random.random() - 2.5
            if x**2 + y**2 < 6.25:
                break
        z = 0.0

        # Random direction in the upper half-space (i.e. from the cathode plane to the anode plane)
        ctheta = np.random.random()
        stheta = np.sqrt(1.0 - ctheta**2)
        phi = 2.0 * np.pi * np.random.random()

        return (x, y, z), (ctheta, stheta, phi)
    
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
        x: float, # mm
        y: float, # mm
        z: float, # mm
        energy: float # MeV
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
        innerAnodeColor: str = "tab:cyan",
        outerAnodeColor: str = "tab:orange",
        differenceColor: str = "tab:brown",
        swapAnodes: bool = False
    ):
        energy = np.append(self.energyBins.lower, self.energyBins.upper[-1])
        inner = np.append(self.innerAnodeSpectrum, self.innerAnodeSpectrum[-1])
        outer = np.append(self.outerAnodeSpectrum, self.outerAnodeSpectrum[-1])

        ax.set_xlabel("Energy (MeV)")
        ax.set_xlim(self.energyBins.lower[0], self.energyBins.upper[-1])
        ax.axhline(0, color = "gray", linewidth = 0.5)

        # Inner anode energy spectrum:

        axInner = ax
        axInner.set_ylabel("Events", color = innerAnodeColor)
        lns1 = axInner.plot(
            energy,
            inner,
            color = innerAnodeColor,
            drawstyle = "steps-post",
            label = "Inner anode"
        )
        axInner.tick_params(axis = "y", labelcolor = innerAnodeColor)
        axInner.grid(axis = "x")
        ylimInner = axInner.get_ylim()

        # Outer anode energy spectrum:

        axOuter = axInner.twinx() # Instantiate a second `Axes` object that shares the same x-axis
        axOuter.set_ylabel("Events", color = outerAnodeColor)
        lns2 = axOuter.plot(
            energy,
            outer,
            color = outerAnodeColor,
            drawstyle = "steps-post",
            label = "Outer anode"
        )
        axOuter.tick_params(axis = "y", labelcolor = outerAnodeColor)
        axOuter.grid(axis = "x")
        ylimOuter = axOuter.get_ylim()

        # Difference:
        
        scale = np.diff(ylimOuter) / np.diff(ylimInner)
        lns3 = axInner.plot(
            energy,
            inner - outer / scale,
            color = differenceColor,
            drawstyle = "steps-post",
            label = "Difference"
        )
        axInner.set_ylim(ylimInner)

        # Legend:

        lns = lns1 + lns2 + lns3
        labels = [l.get_label() for l in lns]
        axOuter.legend(lns, labels, handlelength = 1)