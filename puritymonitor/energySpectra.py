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
    ) -> EnergySpectra:
        if len(self.spectra) != len(self.labels):
            raise ValueError(
                "You must provide an equal number of energy spectra and energy spectra labels."
            )
        
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
    ) -> EnergySpectra:
        with open(filename, "r") as inputFile:
            # Header
            self.labels = next(inputFile).split(",")
            
            # Body (energies and events per energy bin for each spectrum)
            for line in inputFile:
                currentEnergy, *currentSpectra = line.split(",").map(float)
                
        self.energy = energy
        self.spectra = spectra
        return self
