from .PurityMonitor import PurityMonitor
from .. import RadioactiveElectronSource
from .. import Geometry

####################################################################################################

class PurityMonitorInitDecayTimed(PurityMonitor):
    def __init__(
        self,
        radioactiveElectronSource: RadioactiveElectronSource,
        geometry: Geometry
    ) -> None:
        raise NotImplementedError
        super.__init__(
            radioactiveElectronSource = radioactiveElectronSource,
            geometry = geometry
        )
