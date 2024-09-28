import numpy as np
from math import isnan
from matplotlib import pyplot as plt

####################################################################################################

class LAr:
    """
    Set of physical parameters defining the drift of free electrons in a liquid argon volume.
    """
    def __init__(self,
        temperature: float = float("NaN"),          # K
        mobility = None,                            # (cm/µs) / (V/cm)
        electricField: float = float("NaN"),        # V/cm
        driftVelocity: float = float("NaN"),        # cm/µs
        lifetime: float = float("NaN"),             # µs
        attenuationLength: float = float("NaN"),    # cm
        #equivDioxygen: float = float("NaN"),        # ppb
        #equivDioxygenConstant: float = float("NaN") #
    ):
        self.temperature = temperature
        self.mobility = mobility if mobility is not None else self.defaultMobility
        self.electricField = electricField
        self.driftVelocity = driftVelocity
        self.lifetime = lifetime
        self.attenuationLength = attenuationLength
        #self.equivDioxygen = equivDioxygen
        #self.equivDioxygenConstant = equivDioxygenConstant
        
        # Compute all missing physical parameters from the all given ones and an ordered list of
        # mathematical functions defining their relationships
        
        self.functions = [
            self.computeDriftVelocity,
            self.computeElectricField
        ]
        
        for computeVariable in self.functions:
            computeVariable()

    def __str__(self):
        props = (
            ("temperature", "K"),
            ("mobility", ""),
            ("electricField", "V/cm"),
            ("driftVelocity", "cm/µs"),
            ("lifetime", "µs"),
            ("attenuationLength", "cm"),
            #("equivDioxygen", "ppb"),
            #("equivDioxygenConstant", "")
        )
        return "\n".join([
            "LAr volume (",
            ", \n".join([
                f"{prop: <24} = {getattr(self, prop)}{unit}"
                for prop, unit in zip(props)
            ]),
            "\n)"
        ])
        
    @staticmethod
    def defaultMobility(self, temperature: float, electricField: float) -> float:
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
        
    def computeDriftVelocity(self):
        if isnan(self.driftVelocity):
            self.driftVelocity = self.mobility(self.temperature, self.electricField) * self.electricField
        return self.driftVelocity
        
    def computeElectricField(self):
        if isnan(self.electricField):
            self.electricField = self.driftVelocity / self.electronMobility(self.temperature, self.electricField)
        return self.electricField
        
    def computeMobility(self):
        if self.mobility is None:
            self.mobility = lambda temperature, electricField: self.driftVelocity / self.electricField
        return self.mobility
        
    def computeAttenuationLength(self):
        if isnan(self.attenuationLength):
            self.attenuationLength = self.driftVelocity * self.lifetime
        return self.attenuationLength
        
    def computeLifetime(self):
        if isnan(self.lifetime):
            self.lifetime = self.attenuationLength / self.driftVelocity
        return self.lifetime
        
    #def computeEquivDioxygen(self):
    #    return self.equivDioxygen
        
    #def computeEquivDioxygenConstant(self):
    #    return self.equivDioxygenConstant
