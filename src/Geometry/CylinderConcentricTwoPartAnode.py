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
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.driftLength = driftLength
        
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
            *ring(innerRadius = 0, outerRadius = self.innerRadius, z = self.driftLength),
            alpha = 0.5,
            color = "tab:blue",
            shade = False
        )
        ax.plot_surface(
            *ring(innerRadius = self.innerRadius, outerRadius = self.outerRadius, z = self.driftLength),
            alpha = 0.5,
            color = "tab:orange",
            shade = False
        )
        ax.plot_surface(
            *ring(innerRadius = 0, outerRadius = self.outerRadius, z = 0),
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
    
    def emissionVertexAndDirection(
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
