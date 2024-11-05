import numpy as np
from ..EnergySpectra import EnergySpectra, EnergyBins
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
        energyBins: EnergyBins | None = None,
        innerAnodeSpectrum: Iterable[int] = [],
        outerAnodeSpectrum: Iterable[int] = [],
        **kwargs
    ):
        """
        """

        isExpData = True

        if energyBins is None:
            energyBins = self.energyBins
        energy = np.append(energyBins.lower, energyBins.upper[-1])

        if len(innerAnodeSpectrum) == 0 and len(outerAnodeSpectrum) == 0:
            isExpData = False
            innerAnodeSpectrum, outerAnodeSpectrum = self.innerAnodeSpectrum, self.outerAnodeSpectrum
        inner = np.append(innerAnodeSpectrum, innerAnodeSpectrum[-1])
        outer = np.append(outerAnodeSpectrum, outerAnodeSpectrum[-1])

        ax.set_xlabel(xAxisLabel)
        ax.set_xlim(energyBins.lower[0], energyBins.upper[-1])
        ax.axhline(0, **{**{"linewidth": 0.5}, **gridParams})

        # Inner anode energy spectrum:

        axInner = ax
        axInner.set_ylabel(yAxisLabel, color = innerAnodeColor)
        if isExpData and False:
            lns1 = []
            axInner.hlines(
                innerAnodeSpectrum,
                energyBins.lower,
                energyBins.upper,
                color = innerAnodeColor,
                label = innerAnodeLabel
            )
        else:
            lns1 = axInner.plot(
                energy,
                inner,
                color = innerAnodeColor,
                drawstyle = "steps-post",
                label = innerAnodeLabel
            )
        axInner.grid(axis = "x", **{**{"linewidth": 0.5}, **gridParams})
        ylimInner = axInner.get_ylim()

        # Outer anode energy spectrum:

        axOuter = axInner.twinx() # Instantiate a second `Axes` object that shares the same x-axis
        axOuter.set_ylabel(yAxisLabel, color = outerAnodeColor)
        if isExpData and False:
            lns2 = []
            axOuter.hlines(
                outerAnodeSpectrum,
                energyBins.lower,
                energyBins.upper,
                color = outerAnodeColor,
                label = outerAnodeLabel
            )
        else:
            lns2 = axOuter.plot(
                energy,
                outer,
                color = outerAnodeColor,
                drawstyle = "steps-post",
                label = outerAnodeLabel
            )
        axOuter.grid(axis = "x", **{**{"linewidth": 0.5}, **gridParams})
        ylimOuter = axOuter.get_ylim()

        # Difference:
        
        scale = np.diff(ylimOuter) / np.diff(ylimInner)
        if isExpData and False:
            lns3 = []
            axOuter.hlines(
                innerAnodeSpectrum - outerAnodeSpectrum / scale,
                energyBins.lower,
                energyBins.upper,
                color = differenceColor,
                label = differenceLabel
            )
        else:
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
            energyBins,
            innerAnodeSpectrum - outerAnodeSpectrum / scale,
            nPeaks = 2,
            energyStdDev = energyStdDev
        )
        lns4 = axInner.plot(
            energy,
            gaussian,
            label = fittedPeaksLabel((mean1, mean2), (stdDev1, stdDev2)),
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