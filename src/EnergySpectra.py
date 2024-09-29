from typing import Self # For type hint only (Python >= 3.11)
import numpy as np

####################################################################################################

class EnergyBins:
    def __init__(
        self
    ):
        self.lower = None
        self.upper = None
        self.nBins: int = None
        self.binWidth: float = None

    def fromRange(
        self,
        minEnergy: float = 0.0,
        maxEnergy: float = 2.0,
        nBins: int = 100
    ):
        linSpace = np.linspace(start = minEnergy, stop = maxEnergy, num = nBins + 1)
        self.lower = linSpace[:-1]
        self.upper = linSpace[1:]
        self.nBins = nBins
        self.binWidth = (maxEnergy - minEnergy) / nBins
        
####################################################################################################

class EnergySpectra:
    def __init__(
        self,
        energy = None,
        spectra: list | None = None,
        labels: list[str] | None = None
    ) -> None:
        self.energy = energy
        self.spectra = spectra
        self.labels = labels
        
    def save(
        self,
        filename: str
    ) -> Self:
        if len(self.spectra) != len(self.labels):
            raise ValueError(" ".join([
                "You must provide an equal number of",
                "energy spectra and energy spectra labels."
            ]))
        
        with open(filename, "w") as outputFile:
            # Header
            outputFile.write(",".join(self.labels))
            
            # Body (energies and events per energy bin for each spectrum)
            for values in zip(self.energies, *self.spectra):
                outputFile.write("\n" + ",".join(map(str, values)))
        
        return self
        
    def load(
        self,
        filename: str
    ) -> Self:
        with open(filename, "r") as inputFile:
            # Header
            self.labels = next(inputFile).split(",")

            self.energy = []
            self.spectra = [[] for _ in self.labels[1:]]
            
            # Body (energies and events per energy bin for each spectrum)
            for line in inputFile:
                # Read the current bin
                currentEnergy, *currentSpectra = line.split(",").map(float)

                # Update self.energy and self.spectra accordingly
                self.energy.append(currentEnergy)
                for outSpectrum, inSpectrum in zip(currentSpectra, self.spectra):
                    outSpectrum.append(inSpectrum)
        return self
