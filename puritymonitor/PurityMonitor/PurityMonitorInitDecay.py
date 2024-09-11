from .PurityMonitor import PurityMonitor
from .. import RadioactiveElectronSource
from .. import Geometry

####################################################################################################

class PurityMonitorInitDecay(PurityMonitor):
    def __init__(
        self,
        radioactiveElectronSource: RadioactiveElectronSource,
        geometry: Geometry
    ) -> None:
        super.__init__(
            radioactiveElectronSource = radioactiveElectronSource,
            geometry = geometry
        )
        
    def __str__(
        self
    ) -> str:
        return " ".join([
            "{self.radioactiveElectronSource} LAr purity monitor (initial decay only)\n"
        ])
        
    def draw(
        self,
        ax
    ) -> None:
        self.geometry.draw(ax)
