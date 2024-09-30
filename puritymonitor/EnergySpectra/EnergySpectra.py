from typing import Self # For type hint only (Python >= 3.11)
    
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
            raise ValueError("You must provide an equal number of energy spectra and labels.")
        
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
            
            # Body (energies and events per energy bin for each spectrum)
            self.energy = []
            self.spectra = [[] for _ in self.labels[1:]]
            for line in inputFile:
                # Read the current bin
                currentEnergy, *currentSpectra = line.split(",").map(float)

                # Update self.energy and self.spectra accordingly
                self.energy.append(currentEnergy)
                for savedSpectrum, readSpectrum in zip(self.spectra, currentSpectra):
                    savedSpectrum.append(readSpectrum)
        return self
