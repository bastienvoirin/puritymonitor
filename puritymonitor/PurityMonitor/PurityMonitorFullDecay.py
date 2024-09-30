from .PurityMonitor import PurityMonitor
from .. import RadioactiveSource
from .. import Geometry

####################################################################################################

class PurityMonitorFullDecay(PurityMonitor):
    def __init__(
        self,
        radioactiveSource: RadioactiveSource,
        geometry: Geometry
    ) -> None:
        raise NotImplementedError
        super().__init__(
            radioactiveSource = radioactiveSource,
            geometry = geometry
        )
