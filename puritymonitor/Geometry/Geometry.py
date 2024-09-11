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
    x = np.outer(r, np.cos(u))
    y = np.outer(r, np.sin(u))
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
        return self.description
        
    def visualize(
        self,
        ax
    ):
        """
        This method must be implemented in derived classes.
        """
        raise NotImplementedError
