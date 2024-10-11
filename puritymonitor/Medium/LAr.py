from . import Medium
from typing import Callable, Self

# For type hint only
from ..types import (
    float_K,
    float_V,
    float_µs,
    float_cm,
    float_V_per_cm,
    float_cm_per_μs,
    float_cm2_per_μs_per_V
)

####################################################################################################

class LAr(Medium):
    """
    Set of physical parameters defining how free electrons drift in a liquid argon volume.
    """
    def __init__(
        self,
        temperature: float_K = float("NaN"),
        mobility: Callable[[float_K, float_V], float_cm2_per_μs_per_V] = None,
        electricField: float_V_per_cm = float("NaN"),
        driftVelocity: float_cm_per_µs = float("NaN"),
        lifetime: float_µs = float("NaN"),
        attenuationLength: float_cm = float("NaN")
    ):
        super().__init__(
            temperature,
            mobility,
            electricField,
            driftVelocity,
            lifetime,
            attenuationLength
        )
        
    @classmethod
    def defaultMobility(
        cls,
        temperature: float_K,
        electricField: float_V
    ) -> float_cm2_per_μs_per_V:
        """
        """

        a0 = 551.6   # (cm/s) / (V/cm)
        a1 = 7158.3  # (cm/s) / (V/cm)
        a2 = 4440.43 # (cm/s) / (V/cm)
        a3 = 4.29    # (cm/s) / (V/cm)
        a4 = 43.63   # (cm/s) / (V/cm)
        a5 = 0.2053  # (cm/s) / (V/cm)

        refTemperature = 89.0 # K
        E = electricField / 1000.0
        mu = (a0 + a1*E + a2*E**(3/2) + a3*E**(5/2))
        mu /= (1 + (a1/a0)*E + a4*E**2 + a5*E**3)
        mu *= (temperature / refTemperature)**(3/2)

        return mu
