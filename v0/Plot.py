import matplotlib.pyplot as plt
import numpy as np
import CreateAxes as ca
import CreatePlots as cp
import TransparentColormaps as tc
from tqdm import tqdm


# --- Font Settings --- #
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('axes.formatter', limits=(-2, 2))

# --- Create Colormaps --- #
def Opaque(x): return 1
def Linear(x): return x
def Sqrt(x): return np.sqrt(x)
def LinearSymmetric(x): return np.abs(2*x-1)

tc.make_rgb_colormap("GreenBlack", ['g', 0.75, 'g', 'k'])
tc.setAlpha("GreenBlack", Linear)
tc.make_alphablended_cmap("GreenBlack", "GreenBlack_rgb")

tc.setAlpha("RdPu", Sqrt)
tc.make_alphablended_cmap("RdPu", "RdPu_rgb")


#frame = 35
# --- Plot --- #
def Plot(axesSettings, plotSettings, saveFigures=True, i=None):
    dependablePlotSettings = cp.getDependables(plotSettings)
    if i is None:
        for i in tqdm(range(200)):  # [frame]:#
            axes = ca.getAxes(axesSettings)
            cp.add_plots(axes, plotSettings, dependablePlotSettings, i)
            ca.setAxes(axes, axesSettings)

            fig = plt.gcf()
            fig.set_tight_layout(True)
            fig.canvas.draw()
            if saveFigures:
                fig.savefig(str(i) + '.png', dpi=300)
            # plt.show()
            plt.close()
    else:
        axes = ca.getAxes(axesSettings)
        cp.add_plots(axes, plotSettings, dependablePlotSettings, i)
        ca.setAxes(axes, axesSettings)

        fig = plt.gcf()
        fig.set_tight_layout(True)
        fig.canvas.draw()
        if saveFigures:
            fig.savefig(str(i) + '.png', dpi=300)
        # plt.show()
        plt.close()