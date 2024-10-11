from ..types import float_mm, float_MeV # For type hint only
from ..EnergySpectra import EnergyBins, EnergySpectra
from .Geometry import Geometry, cylinder, ring
from .InnerOuterAnodes import InnerOuterAnodes
import numpy as np

####################################################################################################

class CylinderConcentricTwoPartAnode(InnerOuterAnodes):
    """
    Cylindrical TPC geometry with concentric inner disk anode and outer ring anode.
    """

    def __init__(
        self,
        innerRadius: float_mm,
        outerRadius: float_mm,
        driftLength: float_mm
    ):
        super().__init__()
        self.description = "cylindrical geometry with two concentric anodes"
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.driftLength = driftLength
        self.energyBins = EnergyBins()
        
    def __repr__(
        self
    ):
        return "\n".join([
            f"{self.__class__.__name__}(",
            f"  innerRadius = {repr(self.innerRadius)}, # mm",
            f"  outerRadius = {repr(self.outerRadius)}, # mm",
            f"  driftLength = {repr(self.driftLength)}  # mm",
            ")"
        ])
    
    def __eq__(
        self,
        other
    ):
        """
        Equality test between two `CylinderConcentricTwoPartAnode` instances, i.e. whether they
        describe the same geometry. In Python,

        ```
        geometry1 == geometry2
        ```

        calls

        ```
        geometry1.__eq__(geometry2)
        ```
        
        under the hood.
        """

        # Comparison between a `CylinderConcentricTwoPartAnode` instance and any other object is not
        # implemented.
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        return (
                self.innerRadius == self.innerRadius
            and self.outerRadius == self.outerRadius
            and self.driftLength == self.driftLength
        )
    
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
        x: float_mm,
        y: float_mm,
        z: float_mm
    ) -> bool:
        """
        Indicate whether a given 3D point (x, y, z) lies inside the active volume.
        """
        return ((x**2 + y**2) <= self.outerRadius**2) and (0 <= z <= self.driftLength)
    
    def decayVertexAndDirection(
        self
    ) -> tuple[tuple[float_mm, float_mm, float_mm], tuple[float, float, float]]:
        """
        Sample a random IC electron or gamma emission vertex at the surface of the radioactive
        source, and a random direction in the upper half-space (i.e. from the cathode plane to the
        anode plane).
        """

        # Random direction in the upper half-space (i.e. from the cathode plane to the anode plane)
        ctheta = np.random.random()
        stheta = np.sqrt(1.0 - ctheta**2)
        phi = 2.0 * np.pi * np.random.random()

        # Random point (x, y, z = 0) inside a disk of radius squared r² = 6.25
        r = np.random.triangular(0, np.sqrt(6.25), np.sqrt(6.25))
        theta = 2 * np.pi * np.random.random()
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = 0.0

        return (x, y, z), (ctheta, stheta, phi)
    
    def resetAnodeSpectra(
        self,
        nBins: int = 100,
        minEnergy: float_MeV = 0.0,
        maxEnergy: float_MeV = 2.0
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
        x: float_mm,
        y: float_mm,
        z: float_mm,
        energy: float_MeV
    ):
        mask = (energy > self.energyBins.lower) & (energy < self.energyBins.upper)
        if 0 <= z <= self.driftLength:
            if (x**2 + y**2) <= self.innerRadius**2:
                self.innerAnodeSpectrum[mask] += 1
            elif (x**2 + y**2) <= self.outerRadius**2:
                self.outerAnodeSpectrum[mask] += 1
    
    def getAnodeSpectra(
        self
    ):
        """
        """
        return self.innerAnodeSpectrum, self.outerAnodeSpectrum
