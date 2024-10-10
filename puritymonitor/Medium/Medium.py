from math import isnan
from typing import Callable # For type hint only

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

class Medium:
    """
    Set of physical parameters defining free electrons drift in a medium.
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
        temperature: float_K,
        electricField: float_V
    ) -> float_cm2_per_μs_per_V:
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
