from .PurityMonitor import PurityMonitor
from .. import RadioactiveSource
from .. import Geometry

####################################################################################################

class PurityMonitorInitDecay(PurityMonitor):
    def __init__(
        self,
        radioactiveSource: RadioactiveSource,
        geometry: Geometry
    ):
        super().__init__(
            radioactiveSource = radioactiveSource,
            geometry = geometry
        )
        
    def __str__(
        self
    ) -> str:
        """
        """
        return f"purity monitor ({self.radioactiveSource}, {self.geometry}, initial decay only)"
    
    def draw(
        self,
        ax
    ):
        """
        """
        self.geometry.draw(ax)
