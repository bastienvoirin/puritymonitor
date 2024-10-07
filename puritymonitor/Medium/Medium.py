from math import isnan
from typing import Callable # For type hint only

####################################################################################################

class Medium:
    """
    Set of physical parameters defining free electrons drift in a medium.
    """
    def __init__(
        self,
        temperature: float = float("NaN"),                # K
        mobility: Callable[[float, float], float] = None, # (cm/µs) / (V/cm)
        electricField: float = float("NaN"),              # V/cm
        driftVelocity: float = float("NaN"),              # cm/µs
        lifetime: float = float("NaN"),                   # µs
        attenuationLength: float = float("NaN")           # cm
    ):
        self.temperature = temperature
        self.mobility = mobility if mobility is not None else self.defaultMobility
        self.electricField = electricField
        self.driftVelocity = driftVelocity
        self.lifetime = lifetime
        self.attenuationLength = attenuationLength
        
        # Compute all missing physical parameters from the all given ones and an ordered list of
        # mathematical functions defining their relationships
        
        self.functions = [
            self.computeDriftVelocity,
            self.computeElectricField
        ]
        
        for computeVariable in self.functions:
            computeVariable()

    def __str__(
        self
    ) -> str:
        """
        """
        return "LAr volume"
    
    def __repr__(
        self
    ) -> str:
        """
        """
        props = (
            ("temperature", "K"),
            ("mobility", "(cm/µs) / (V/cm)"),
            ("electricField", "V/cm"),
            ("driftVelocity", "cm/µs"),
            ("lifetime", "µs"),
            ("attenuationLength", "cm")
        )
        return "\n".join([
            "LAr(",
            *[
                f"  {prop} = {getattr(self, prop)}, # {unit}"
                for prop, unit in zip(props)
            ],
            ")"
        ])
    
    @staticmethod
    def defaultMobility(
        temperature: float,
        electricField: float
    ) -> float:
        """
        """
        raise NotImplementedError
        
    def computeDriftVelocity(self):
        if isnan(self.driftVelocity):
            self.driftVelocity = self.electricField * self.mobility(
                self.temperature,
                self.electricField
            )
        return self.driftVelocity
        
    def computeElectricField(self):
        if isnan(self.electricField):
            self.electricField = self.driftVelocity / self.mobility(
                self.temperature,
                self.electricField
            )
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
