from typing import Self # For type hint only (Python >= 3.11)
from . import EnergyBins
import numpy as np
from scipy.optimize import curve_fit

####################################################################################################

def gaussian(x, *params):
    """
    Compute a Gaussian.
    """
    a, mu, sigma = params
    return a * np.exp(-(x - mu)**2 / (2.0 * sigma**2))

####################################################################################################

class EnergySpectra:
    def __init__(
        self,
        energyBins: EnergyBins = None,
        spectra: list = None,
        labels: list[str] = None
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
            raise ValueError("You must provide an equal number of energy spectra and labels.")
        
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

    @staticmethod
    def fit(
        energyBins: EnergyBins,
        spectrum,
        initialGuess: tuple[float, float, float] = (None, None, None)
    ):
        """
        Usage:

        ```
        EnergySpectra.fit(energyBins, spectrum, initialGuess)
        ```

        or

        ```
        EnergySpectra().fit(energyBins, spectrum, initialGuess)
        ```
        """

        a, mu, sigma = initialGuess
        argmax = np.argmax(spectrum)
        a = a if a is not None else spectrum[argmax]
        mu = mu if mu is not None else (energyBins.lower[argmax] + energyBins.upper[argmax]) / 2
        sigma = sigma if sigma is not None else 0.5
        
        params, _ = curve_fit(
            f = gaussian,
            xdata = (energyBins.lower + energyBins.upper) / 2,
            ydata = spectrum,
            p0 = (a, mu, sigma)
        )
        energies = np.linspace(energyBins.lower[0], energyBins.upper[-1], 1000)
        fitted = gaussian(energies, *params)
        
        return params, energies, fitted