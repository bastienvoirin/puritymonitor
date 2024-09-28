from .. import RadioactiveSource
from .. import Geometry

####################################################################################################

class PurityMonitor:
    def __init__(
        self,
        radioactiveSource: RadioactiveSource,
        geometry: Geometry
    ) -> None:
        self.radioactiveSource = radioactiveSource
        self.geometry = geometry
        
    def __str__(
        self
    ) -> str:
        return " ".join([
            "{self.radioactiveSource} LAr purity monitor\n"
        ])
        
    def draw(
        self,
        ax
    ) -> None:
        self.geometry.draw(ax)
