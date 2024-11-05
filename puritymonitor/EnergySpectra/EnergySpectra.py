from sys import stderr
from . import EnergyBins
import numpy as np
from scipy.optimize import curve_fit
from typing import Self # For type hint only (Python >= 3.11)
from collections.abc import Iterable
from ..types import float_MeV # For type hint only

####################################################################################################

def gaussian(
        x,
        amplitude: float,
        mean: float,
        stdDev: float
    ):
    """
    Compute a Gaussian of given amplitude, mean, and standard deviation.
    """
    return amplitude * np.exp(-(x - mean)**2 / (2.0 * stdDev**2))

####################################################################################################

def doubleGaussian(
        x,
        amplitude1: float,
        mean1: float,
        stdDev1: float,
        amplitude2: float,
        mean2: float,
        stdDev2: float
    ):
    """
    Compute a double Gaussian of given amplitudes, means, and standard deviations.
    """
    gaussian1 = amplitude1 * np.exp(-(x - mean1)**2 / (2.0 * stdDev1**2))
    gaussian2 = amplitude2 * np.exp(-(x - mean2)**2 / (2.0 * stdDev2**2))
    return gaussian1 + gaussian2

####################################################################################################

class EnergySpectra:
    """
    """

    def __init__(
        self,
        energyBins: EnergyBins,
        spectra: Iterable = [],
        labels: Iterable[str] = []
    ):
        self.energyBins = energyBins
        self.spectra = spectra
        self.labels = labels
        
    def __str__(
        self
    ) -> str:
        """
        Readable representation of an `EnergySpectra` instance.
        """
        return f"EnergySpectra({", ".join(self.labels)}; {str(self.energyBins)})"
    
    def __repr__(
        self
    ) -> str:
        """
        Unambiguous, explicit string representation of an `EnergySpectra` instance.
        """
        return "\n".join([
            "EnergySpectra(",
            f"  energyBins = {repr(self.energyBins)},",
            f"  spectra = {repr(self.spectra)},",
            f"  labels = {repr(self.labels)}",
            ")"
        ])
    
    def save(
        self,
        filename: str
    ) -> Self:
        """
        Save the energy spectra to a `csv` file or any other text-based file.
        """

        if len(self.spectra) != len(self.labels):
            raise ValueError("You must provide an equal number of energy spectra and energy spectra labels.")
        
        with open(filename, "w") as outputFile:
            # Header
            outputFile.write(",".join(self.labels))
            
            # Body (energies and events per energy bin for each spectrum)
            for values in zip(self.energyBins.lower, *self.spectra):
                outputFile.write("\n" + ",".join(map(str, values)))
        
        return self
        
    @staticmethod
    def load(
        filename: str,
        ignore: Iterable[int] = []
    ) -> Self:
        """
        Load energy spectra from a `csv` file or any other text-based file.
        """

        lowerEnergy = []

        with open(filename, "r") as inputFile:
            # Header (labels for the energy column and each spectrum)
            labels = [
                label
                for index, label in enumerate(next(inputFile).strip().split(","))
                if index not in ignore
            ]
            
            # Body (energies and events per energy bin for each spectrum)
            energy = []
            spectra = [
                []
                for index, _ in enumerate(labels[1:])
                if index not in ignore
            ]
            for line in inputFile:
                # Read the current bin
                currentEnergy, *currentSpectra = [
                    0.0 if value == "" or value == "\n" else float(value)
                    for index, value in enumerate(line.strip().split(","))
                    if index not in ignore
                ]

                # Update self.energy and self.spectra accordingly
                lowerEnergy.append(currentEnergy)
                for savedSpectrum, readSpectrum in zip(spectra, currentSpectra):
                    savedSpectrum.append(readSpectrum)

        return EnergySpectra(
            energyBins = EnergyBins.fromLower(lowerEnergy),
            spectra = spectra,
            labels = labels
        )

    @classmethod
    def fit(
        cls,
        energyBins: EnergyBins,
        spectrum,
        energyStdDev: float_MeV,
        nPeaks: int = 1,
        initialGuess1: tuple[float, float, float] = (None, None, None),
        initialGuess2: tuple[float, float, float] = (None, None, None)
    ):
        """
        Usage:

        ```
        EnergySpectra.fit(energyBins, spectrum, initialGuess)
        ```
        """

        if nPeaks != 1 and nPeaks != 2:
            raise ValueError(f"Fitting with `nPeaks = {nPeaks}` is not supported. `nPeaks` should be either 1 or 2.")

        amplitude1, mean1, stdDev1 = initialGuess1
        amplitude2, mean2, stdDev2 = initialGuess2

        argmax = np.argmax(spectrum)

        amplitude1 = amplitude1 if amplitude1 is not None else spectrum[argmax]
        mean1 = mean1 if mean1 is not None else (energyBins.lower[argmax] + energyBins.upper[argmax]) / 2
        stdDev1 = stdDev1 if stdDev1 is not None else energyStdDev

        amplitude2 = amplitude2 if amplitude2 is not None else amplitude1 / 5
        mean2 = mean2 if mean2 is not None else mean1 / 2
        stdDev2 = stdDev2 if stdDev2 is not None else stdDev1

        if nPeaks == 1:
            print(f"Guess: amplitude = {amplitude1}, mean = {mean1}, standard deviation = {stdDev1}")
        if nPeaks == 2:
            print(f"Guess:")
            print(f"  amplitude = {amplitude1}, mean = {mean1}, standard deviation = {stdDev1}")
            print(f"  amplitude = {amplitude2}, mean = {mean2}, standard deviation = {stdDev2}")

        try:
            if nPeaks == 1:
                (amplitude1, mean1, stdDev1), _ = curve_fit(
                    f = gaussian,
                    xdata = (energyBins.lower + energyBins.upper) / 2,
                    ydata = spectrum,
                    p0 = (amplitude1, mean1, stdDev1)
                )
            elif nPeaks == 2:
                (amplitude1, mean1, stdDev1, amplitude2, mean2, stdDev2), _ = curve_fit(
                    f = doubleGaussian,
                    xdata = (energyBins.lower + energyBins.upper) / 2,
                    ydata = spectrum,
                    p0 = (amplitude1, mean1, stdDev1, amplitude2, mean2, stdDev2)
                )
        except RuntimeError:
            print("Error: Gaussian fit of the IC peak(s) failed.", file = stderr)

        print(f"Fit:")
        print(f"  amplitude = {amplitude1}, mean = {mean1}, standard deviation = {stdDev1}")
        if nPeaks == 2:
            print(f"  amplitude = {amplitude2}, mean = {mean2}, standard deviation = {stdDev2}")

        energies = np.linspace(energyBins.lower[0], energyBins.upper[-1], 1000)

        if nPeaks == 1:
            fitted = gaussian(energies, amplitude1, mean1, stdDev1)
        elif nPeaks == 2:
            fitted = doubleGaussian(energies, amplitude1, mean1, stdDev1, amplitude2, mean2, stdDev2)
        
        return (amplitude1, mean1, stdDev1), (amplitude2, mean2, stdDev2), energies, fitted