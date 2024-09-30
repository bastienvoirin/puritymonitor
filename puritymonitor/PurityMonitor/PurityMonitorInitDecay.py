from .PurityMonitor import PurityMonitor
from .. import RadioactiveSource
from .. import Geometry

####################################################################################################

class PurityMonitorInitDecay(PurityMonitor):
    def __init__(
        self,
        radioactiveSource: RadioactiveSource,
        geometry: Geometry
    ) -> None:
        super().__init__(
            radioactiveSource = radioactiveSource,
            geometry = geometry
        )
        
    def __str__(
        self
    ) -> str:
        return " ".join([
            "{self.radioactiveSource} LAr purity monitor (initial decay only)\n"
        ])
        
    def draw(
        self,
        ax
    ) -> None:
        self.geometry.draw(ax)
