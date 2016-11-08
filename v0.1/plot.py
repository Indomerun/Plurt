import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import TransparentColormaps as tc

from dependables import calculate_dependables
from createaxes import createAxes
from createplots import add_plots
from setaxes import setAxes

from tqdm import tqdm


# --- Text Settings --- #
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
    for settings in axesSettings + plotSettings:
        settings.map_settings()
    calculate_dependables(axesSettings, plotSettings)

    if i is None:
        for i in tqdm(range(200)):  # [frame]:#
            axes = createAxes(axesSettings)
            add_plots(axes, plotSettings, i)
            setAxes(axes, axesSettings)

            fig = plt.gcf()
            fig.set_tight_layout(True)
            fig.canvas.draw()
            if saveFigures:
                fig.savefig(str(i) + '.png', dpi=300)
            # plt.show()
            plt.close()
    else:
        axes = createAxes(axesSettings)
        add_plots(axes, plotSettings, i)
        setAxes(axes, axesSettings)

        #axes['XY'].set_axis_off()

        fig = plt.gcf()
        fig.set_tight_layout(True)
        fig.canvas.draw()
        if saveFigures:
            fig.savefig(str(i) + '.png', dpi=300)
        # plt.show()
        plt.close()


# TODO: Add ParticleTracks
# TODO: Add multiprocessing
# TODO: Implement alternative "alpha"-blending
# TODO: Add 'zorder' for manual control of what will be on top
# TODO: Move cmap creation from plot.py
