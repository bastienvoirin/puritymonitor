from .. import RadioactiveElectronSource
from .. import Geometry

####################################################################################################

class PurityMonitor:
    def __init__(
        self,
        radioactiveElectronSource: RadioactiveElectronSource,
        geometry: Geometry
    ) -> None:
        self.radioactiveElectronSource = radioactiveElectronSource
        self.geometry = geometry
        
    def __str__(
        self
    ) -> str:
        return " ".join([
            "{self.radioactiveElectronSource} LAr purity monitor\n"
        ])
        
    def draw(
        self,
        ax
    ) -> None:
        self.geometry.draw(ax)
