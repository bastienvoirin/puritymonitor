import numpy as np
from ..EnergySpectra import EnergyBins
from collections.abc import Iterable # For type hint only
from ..types import float_mm, float_MeV # For type hint only

####################################################################################################

def cylinder(
    radius: float = 10.0,
    height: float = 100.0,
    centerX: float = 0.0,
    centerY: float = 0.0
):
    """
    """
    z = np.linspace(0, height, 10)
    theta = np.linspace(0, 2*np.pi, 100)
    thetaCyl, zCyl = np.meshgrid(theta, z)
    xCyl = centerX + radius * np.cos(thetaCyl)
    yCyl = centerY + radius * np.sin(thetaCyl)
    return xCyl, yCyl, zCyl

####################################################################################################

def ring(
    innerRadius: float = 10.0,
    outerRadius: float = 20.0,
    planeZ: float = 0.0,
    centerX: float = 0.0,
    centerY: float = 0.0
):
    """
    """
    r = np.linspace(innerRadius, outerRadius, 10)
    u = np.linspace(0, 2*np.pi, 100)
    x = centerX + np.outer(r, np.cos(u))
    y = centerY + np.outer(r, np.sin(u))
    return x, y, np.full(x.shape, planeZ)

####################################################################################################

class Geometry:
    """
    Abstract base class to inherit from and implement.
    """
    def __init__(
        self
    ):
        self.description = "geometry"
        self.energyBins = EnergyBins(
            lower = [],
            upper = [],
            nBins = np.nan,
            binWidth = np.nan
        )
        
    def __str__(
        self
    ):
        """
        """
        return self.description
        
    def __repr__(
        self
    ):
        """
        """
        return self.__class__.__name__ + "()"
        
    def __eq__(
        self,
        other
    ):
        """
        Equality test between two `Geometry` instances, i.e. whether they describe the same
        geometry. In Python,

        ```
        geometry1 == geometry2
        ```

        calls

        ```
        geometry1.__eq__(geometry2)
        ```
        
        under the hood.
        
        This method must be implemented in derived classes.
        """

        # Comparison between a `Geometry` instance and any other object is not implemented.
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        
        raise NotImplementedError
    
    def draw(
        self,
        ax
    ):
        """
        Draw the geometry.
        
        This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    def isInsideActiveVolume(
        self,
        x: float_mm,
        y: float_mm,
        z: float_mm
    ):
        """
        Indicate whether a given 3D point (x, y, z) lies inside the active volume.
        
        This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    def decayVertexAndDirection(
        self
    ) -> tuple[tuple[float_mm, float_mm, float_mm], tuple[float, float, float]]:
        """
        Sample a random IC electron or gamma emission vertex at the surface of the radioactive
        source, and a random direction in the upper half-space (i.e. from the cathode plane to the
        anode plane).

        This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    def resetAnodeSpectra(
        self,
        nBins: int = 100,
        minEnergy: float_MeV = 0.0,
        maxEnergy: float_MeV = 2.0
    ) -> None:
        """
        This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    def updateAnodeSpectra(
        self
    ) -> None:
        """
        This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    @property
    def anodeSpectra(
        self
    ) -> tuple[Iterable[int]]:
        return self.getAnodeSpectra()
    
    def getAnodeSpectra(
        self
    ) -> tuple[Iterable[int]]:
        """
        This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    def plotAnodeSpectra(
        self
    ) -> None:
        """
        This method must be implemented in derived classes.
        """
        raise NotImplementedError