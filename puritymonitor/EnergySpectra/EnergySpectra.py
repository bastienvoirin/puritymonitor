from typing import Self # For type hint only (Python >= 3.11)
from . import EnergyBins
import numpy as np
from scipy.optimize import curve_fit

####################################################################################################

def gaussian(
        x,
        amplitude: float,
        mean: float,
        std_dev: float
    ):
    """
    Compute a Gaussian.
    """
    return amplitude * np.exp(-(x - mean)**2 / (2.0 * std_dev**2))

####################################################################################################

class EnergySpectra:
    def __init__(
        self,
        energyBins: EnergyBins = None,
        spectra: list = [],
        labels: list[str] = []
    ) -> None:
        self.energyBins = energyBins
        self.spectra = spectra
        self.labels = labels
        
    def save(
        self,
        filename: str
    ) -> Self:
        """
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
        
    def load(
        self,
        filename: str
    ) -> Self:
        """
        """
        lowerEnergy = []
        with open(filename, "r") as inputFile:
            # Header
            self.labels = next(inputFile).split(",")
            
            # Body (energies and events per energy bin for each spectrum)
            self.energy = []
            self.spectra = [[] for _ in self.labels[1:]]
            for line in inputFile:
                # Read the current bin
                currentEnergy, *currentSpectra = line.split(",").map(float)

                # Update self.energy and self.spectra accordingly
                lowerEnergy.append(currentEnergy)
                for savedSpectrum, readSpectrum in zip(self.spectra, currentSpectra):
                    savedSpectrum.append(readSpectrum)
        self.energyBins = EnergyBins() # To do
        return self

    @classmethod
    def fit(
        cls,
        energyBins: EnergyBins,
        spectrum,
        initialGuess: tuple[float, float, float] = (None, None, None)
    ):
        """
        Usage:

        ```
        EnergySpectra.fit(energyBins, spectrum, initialGuess)
        ```
        """

        amplitude, mean, std_dev = initialGuess

        argmax = np.argmax(spectrum)

        amplitude = amplitude if amplitude is not None else spectrum[argmax]
        mean = mean if mean is not None else (energyBins.lower[argmax] + energyBins.upper[argmax]) / 2
        std_dev = std_dev if std_dev is not None else 0.5
        
        try:
            (amplitude, mean, std_dev), _ = curve_fit(
                f = gaussian,
                xdata = (energyBins.lower + energyBins.upper) / 2,
                ydata = spectrum,
                p0 = (amplitude, mean, std_dev)
            )
        except RuntimeError:
            print("Error: Gaussian fit failed.")

        energies = np.linspace(energyBins.lower[0], energyBins.upper[-1], 1000)
        fitted = gaussian(energies, amplitude, mean, std_dev)
        
        return (amplitude, mean, std_dev), energies, fitted