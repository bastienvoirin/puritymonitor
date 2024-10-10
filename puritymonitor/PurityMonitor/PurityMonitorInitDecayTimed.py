from .PurityMonitor import PurityMonitor
from .. import RadioactiveSource
from .. import Geometry

####################################################################################################

class PurityMonitorInitDecayTimed(PurityMonitor):
    def __init__(
        self,
        radioactiveSource: RadioactiveSource,
        geometry: Geometry
    ):
        raise NotImplementedError
        super().__init__(
            radioactiveSource = radioactiveSource,
            geometry = geometry
        )
