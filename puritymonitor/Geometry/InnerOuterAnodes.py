import numpy as np
from ..EnergySpectra import EnergySpectra
from .Geometry import Geometry
from collections.abc import Iterable, Callable # For type hint only
from ..types import float_MeV # For type hint only

####################################################################################################

class InnerOuterAnodes(Geometry):
    """
    Inner and outer anodes.
    """

    def __init__(
        self,
    ):
        super().__init__()
        self.innerAnodeSpectrum: Iterable[int] = []
        self.outerAnodeSpectrum: Iterable[int] = []

    def plotAnodeSpectra(
        self,
        ax,
        energyStdDev: float_MeV,
        xAxisLabel: str = "Energy (MeV)",
        yAxisLabel: str = "Events",
        frameColor: str = "",
        gridParams = {},
        innerAnodeColor: str = "tab:cyan",
        outerAnodeColor: str = "tab:orange",
        differenceColor: str = "tab:brown",
        fittedPeaksColor: str = "tab:green",
        innerAnodeLabel: str = "Inner anode",
        outerAnodeLabel: str = "Outer anode",
        differenceLabel: str = "Difference",
        fittedPeaksLabel: Callable[[Iterable[float_MeV], Iterable[float_MeV]], str] =
            lambda means, stdDevs: "IC peaks fit",
        legendTitle: str = "",
        legendFontSize: int | None = None,
        **kwargs
    ):
        """
        """

        energy = np.append(self.energyBins.lower, self.energyBins.upper[-1])
        inner = np.append(self.innerAnodeSpectrum, self.innerAnodeSpectrum[-1])
        outer = np.append(self.outerAnodeSpectrum, self.outerAnodeSpectrum[-1])

        ax.set_xlabel(xAxisLabel)
        ax.set_xlim(self.energyBins.lower[0], self.energyBins.upper[-1])
        ax.axhline(0, color = "gray", linewidth = 0.5)

        """
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
        """

        # Inner anode energy spectrum:

        axInner = ax
        axInner.set_ylabel(yAxisLabel, color = innerAnodeColor)
        lns1 = axInner.plot(
            energy,
            inner,
            color = innerAnodeColor,
            drawstyle = "steps-post",
            label = innerAnodeLabel
        )
        axInner.grid(axis = "x", **gridParams)
        ylimInner = axInner.get_ylim()

        # Outer anode energy spectrum:

        axOuter = axInner.twinx() # Instantiate a second `Axes` object that shares the same x-axis
        axOuter.set_ylabel(yAxisLabel, color = outerAnodeColor)
        lns2 = axOuter.plot(
            energy,
            outer,
            color = outerAnodeColor,
            drawstyle = "steps-post",
            label = outerAnodeLabel
        )
        axOuter.grid(axis = "x", **gridParams)
        ylimOuter = axOuter.get_ylim()

        # Difference:
        
        scale = np.diff(ylimOuter) / np.diff(ylimInner)
        lns3 = axInner.plot(
            energy,
            inner - outer / scale,
            color = differenceColor,
            drawstyle = "steps-post",
            label = differenceLabel
        )
        axInner.set_ylim(ylimInner)

        # Gaussian fit of the ~1 MeV peaks:

        (_, mean1, stdDev1), (_, mean2, stdDev2), energy, gaussian = EnergySpectra.fit(
            self.energyBins,
            self.innerAnodeSpectrum - self.outerAnodeSpectrum / scale,
            nPeaks = 2,
            energyStdDev = energyStdDev
        )
        lns4 = axInner.plot(
            energy,
            gaussian,
            label = fittedPeaksLabel((mean1, mean2), (stdDev1, stdDev1)),
            color = fittedPeaksColor
        )

        # Legend:

        lns = lns1 + lns2 + lns3 + lns4
        legend = axOuter.legend(
            lns,
            map(lambda ln: ln.get_label(), lns),
            handlelength = 1,
            borderaxespad = 0.1,
            fancybox = False,
            alignment = "left",
            title = legendTitle,
            **({"title_fontsize": legendFontSize} if legendFontSize is not None else {}),
            prop = {"size": legendFontSize} if legendFontSize is not None else {}
        )
        legend.get_frame().set_linewidth(0)
        legend._legend_box.align = "left"

        axInner.tick_params(axis = "y", color = frameColor, labelcolor = innerAnodeColor)
        axOuter.tick_params(axis = "y", color = frameColor, labelcolor = outerAnodeColor)
        for ax in (ax, axInner, axOuter):
            ax.tick_params(color = frameColor, labelcolor = frameColor, axis = "x")
            for spine in ax.spines.values():
                spine.set_edgecolor(frameColor)