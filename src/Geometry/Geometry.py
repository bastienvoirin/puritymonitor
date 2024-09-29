import numpy as np

####################################################################################################

def cylinder(
    centerX: float = 0.0,
    centerY: float = 0.0,
    radius: float = 10.0,
    height: float = 100.0
):
    z = np.linspace(0, height, 10)
    theta = np.linspace(0, 2*np.pi, 100)
    thetaCyl, zCyl = np.meshgrid(theta, z)
    xCyl = centerX + radius * np.cos(thetaCyl)
    yCyl = centerY + radius * np.sin(thetaCyl)
    return xCyl, yCyl, zCyl

####################################################################################################

def ring(
    centerX: float = 0.0,
    centerY: float = 0.0,
    planeZ: float = 0.0,
    innerRadius: float = 10.0,
    outerRadius: float = 20.0
):
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
    def __init__(self):
        self.description = "Geometry"
        
    def __str__(self):
        return self.description
        
    def __repr__(self):
        return self.description + "()"
        
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
        x: float,
        y: float,
        z: float
    ):
        """
        Indicate whether a given 3D point (x, y, z) lies inside the active volume.
        
        This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    def decayVertexAndDirection(
        self
    ) -> tuple[tuple[float, float, float], tuple[float, float]]:
        """
        Sample a random IC electron or gamma emission vertex at the surface of the radioactive
        source, and a random direction in the upper half-space (i.e. from the cathode plane to the
        anode plane).

        This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    def resetAnodeSpectra(
        self,
        nPoints: int = 100,
        minEnergy: float = 0.0,
        maxEnergy: float = 2.0,
        energyScale: float = 1.0
    ):
        """
        This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    def updateAnodeSpectra(
        self
    ):
        """
        This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    def getAnodeSpectra(
        self
    ):
        """
        This method must be implemented in derived classes.
        """
        raise NotImplementedError