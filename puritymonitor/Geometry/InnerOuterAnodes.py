from ..types import float_mm, float_MeV # For type hint only
from ..EnergySpectra import EnergyBins, EnergySpectra
from .Geometry import Geometry
import numpy as np

####################################################################################################

class InnerOuterAnodes(Geometry):
    """
    Inner and outer anodes.
    """

    def __init__(
        self,
    ):
        super().__init__()
        self.innerAnodeSpectrum = []
        self.outerAnodeSpectrum = []

    def plotAnodeSpectra(
        self,
        ax,
        innerAnodeColor: str = "tab:cyan",
        outerAnodeColor: str = "tab:orange",
        differenceColor: str = "tab:brown",
        fittedPeakColor: str = "tab:green",
        **kwargs
    ):
        """
        """

        energy = np.append(self.energyBins.lower, self.energyBins.upper[-1])
        inner = np.append(self.innerAnodeSpectrum, self.innerAnodeSpectrum[-1])
        outer = np.append(self.outerAnodeSpectrum, self.outerAnodeSpectrum[-1])

        ax.set_xlabel("Energy (MeV)")
        ax.set_xlim(self.energyBins.lower[0], self.energyBins.upper[-1])
        ax.axhline(0, color = "gray", linewidth = 0.5)
        def events(nEvents):
            pow = 0
            while nEvents % 1000 == 0:
                pow += 3
                nEvents //= 1000
            return f"{nEvents}{({0: "", 3: "k", 6: "M"}[pow])}"
        ax.text(
            0.0,
            1.01,
            r"\textbf{Simulation}" + f" ({events(kwargs["nEvents"])} events)",
            ha = "left",
            va = "bottom",
            transform = ax.transAxes
        )
        ax.text(
            1.0,
            1.01,
            f"$\\ell_{{\\mathrm{{drift}}}} = {int(round(self.driftLength))}\\mathrm{{mm}}$",
            ha = "right",
            va = "bottom",
            transform = ax.transAxes
        )

        # Inner anode energy spectrum:

        axInner = ax
        axInner.set_ylabel("Events", color = innerAnodeColor)
        lns1 = axInner.plot(
            energy,
            inner,
            color = innerAnodeColor,
            drawstyle = "steps-post",
            label = "Inner anode"
        )
        axInner.tick_params(axis = "y", labelcolor = innerAnodeColor)
        axInner.grid(axis = "x")
        ylimInner = axInner.get_ylim()

        # Outer anode energy spectrum:

        axOuter = axInner.twinx() # Instantiate a second `Axes` object that shares the same x-axis
        axOuter.set_ylabel("Events", color = outerAnodeColor)
        lns2 = axOuter.plot(
            energy,
            outer,
            color = outerAnodeColor,
            drawstyle = "steps-post",
            label = "Outer anode"
        )
        axOuter.tick_params(axis = "y", labelcolor = outerAnodeColor)
        axOuter.grid(axis = "x")
        ylimOuter = axOuter.get_ylim()

        # Difference:
        
        scale = np.diff(ylimOuter) / np.diff(ylimInner)
        lns3 = axInner.plot(
            energy,
            inner - outer / scale,
            color = differenceColor,
            drawstyle = "steps-post",
            label = "Difference"
        )
        axInner.set_ylim(ylimInner)

        # Gaussian fit of the ~1 MeV peak:

        (_, peakEnergy, _), energy, gaussian = EnergySpectra.fit(
            self.energyBins,
            self.innerAnodeSpectrum - self.outerAnodeSpectrum / scale
        )
        lns4 = axInner.plot(energy, gaussian, label = "Gaussian peak", color = fittedPeakColor)

        # Legend:

        lns = lns1 + lns2 + lns3 + lns4
        axOuter.legend(
            lns,
            map(lambda ln: ln.get_label(), lns),
            handlelength = 1,
            borderaxespad = 0.1,
            fancybox = False
        ).get_frame().set_linewidth(0)