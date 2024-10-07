from . import Medium

####################################################################################################

class LAr(Medium):
    """
    Set of physical parameters defining how free electrons drift in a liquid argon volume.
    """
    def __init__(
        self,
        temperature: float = float("NaN"),      # K
        mobility = None,                        # (cm/µs) / (V/cm)
        electricField: float = float("NaN"),    # V/cm
        driftVelocity: float = float("NaN"),    # cm/µs
        lifetime: float = float("NaN"),         # µs
        attenuationLength: float = float("NaN") # cm
    ):
        super().__init__(
            temperature,
            mobility,
            electricField,
            driftVelocity,
            lifetime,
            attenuationLength
        )
        
    @staticmethod
    def defaultMobility(
        temperature: float,
        electricField: float
    ) -> float:
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
