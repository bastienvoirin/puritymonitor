from .Geometry import Geometry, cylinder, ring

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
        self.innerRadius = innerRadius
        self.driftLength = driftLength
        
    def visualize(
        self,
        ax
    ):
        ax.plot_surface(*cylinder(radius = outerRadius, height = height), alpha = 0.125, color = "k", shade = False)
        ax.plot_surface(*ring(innerRadius = 0, outerRadius = innerRadius, z = height), alpha = 0.5, color = "tab:blue", shade = False)
        ax.plot_surface(*ring(innerRadius = innerRadius, outerRadius = outerRadius, z = height), alpha = 0.5, color = "tab:orange", shade = False)
        ax.plot_surface(*ring(innerRadius = 0, outerRadius = outerRadius, z = 0), alpha = 0.25, color = "k", shade = False)
        ax.plot([0], [0], [0], alpha = 1., markerfacecolor = "tab:green", markeredgecolor = "tab:green", marker = "o")
        
        # Equal axes (https://github.com/matplotlib/matplotlib/issues/17172#issuecomment-830139107)
        ax.set_box_aspect([
            upperBound - lowerBound
            for lowerBound, upperBound in (getattr(ax, f"get_{axis}lim")() for axis in "xyz")
        ])
        
    def isInside(
        self,
        x: float,
        y: float,
        z: float
    ):
        return ((x**2 + y**2) <= self.outerRadius**2) and (0 <= z <= self.driftLength)
