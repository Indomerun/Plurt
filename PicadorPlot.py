import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from tqdm import tqdm
#from matplotlib.collections import LineCollection

from matplotlib.image import NonUniformImage

import time
import multiprocessing

import TransparentColormaps as tc
import ParticleTracks as pt

def plot2D(i):
    # Declare structs
    data = {}
    data_RGBA = {}

    # Declare the figure
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    fig, ax = plt.subplots(nrows=1)

    ## load data
    for folder in dataFolders:
        Current_filename = files[i]
        data[folder] = (np.fromfile(folder + dirDiv + Current_filename, dtype='f')).reshape(size[folder])

    ## data -> pdata -> rgba -> rgb
    for idx, pName in enumerate(pNames):
        if pName == 'tracks':
            trackDataMatrix, trackAlpha = pt.getTrackMatrix(i, trackData, tracksFadeFactor, tracksCutoff, matrixRange)
            pData[pName] = trackDataMatrix
        else:
            pData[pName] = data[pName]

        data_RGBA[pName] = customDataMapper[pName].to_rgba(pData[pName])
        if pName == 'tracks':
            data_RGBA[pName][..., 3] = trackAlpha

        if idx == 0:
            background = np.ones(data_RGBA[pName].shape)
            data_RGB = tc.alphaBlend(data_RGBA[pName], background)
        else:
            data_RGB = tc.alphaBlend(data_RGBA[pName], data_RGB)

    # Plot rgb data
    #if i == 0:
    im = NonUniformImage(ax)
    im.set_data(x, y, data_RGB)
    ax.images.append(im)

    #trackax = {}
    #for track in trackFiles[::trackSkip]:
    #    points = np.array([trackData[track][:1, 0] / 1e-4, trackData[track][:1, 1] / 1e-4]).T.reshape(-1, 1, 2)
    #    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    #    trackax[track] = LineCollection(segments, array=trackData[track][:1, 6] / MeV, cmap=('tracks' + "_alpha"),
    #                                    norm=custom_norm['tracks'])
    #    ax.add_collection(trackax[track])

    ax.set_xlim(plotExtent[0], plotExtent[1])
    ax.set_ylim(plotExtent[2], plotExtent[3])
    ax.set_aspect('equal')

    ax.set_xlabel(r'$x$ ($\mu$m)')
    ax.set_ylabel(r'$y$ ($\mu$m)')
    for pName in pNames:
        if cbar[pName]:
            plt.colorbar(custom_cbar[pName], ax=ax, shrink=0.52, label=cbar_label[pName])
    fig.set_tight_layout(True)

    #else:
    #    im.set_data(x, y, data_RGB)
        #for track in trackFiles[::trackSkip]:
        #    points = np.array([trackData[track][max(0,i-10):i+1, 0] / 1e-4, trackData[track][max(0,i-10):i+1, 1] / 1e-4]).T.reshape(-1, 1, 2)
        #    segments = np.concatenate([points[:-1], points[1:]], axis=1)
        #    trackax[track].set_segments(segments)
        #    trackax[track].set_array(trackData[track][max(0,i-10):i+1, 6] / MeV)

    ax.set_title("Frame " + str(i))
    #fig.show()
    fig.canvas.draw()
    fig.savefig(os.path.splitext(Current_filename)[0] + '.png', dpi=300)
    print("Saved " + str(i) + "!")
    plt.close()

# Create new colormaps
tc.make_rgb_colormap("GreenBlack", ['g', 0.75, 'g', 'k'])
tc.make_rgb_colormap("RedBlack", ['r', 0.75, 'r', 'k'])

# Declare structs
size = {}
pData = {}
cmap = {}
clim = {}
cmapNorm = {}
cbar = {}
alpha = {}

custom_cmap = {}
custom_norm = {}
customDataMapper = {}
custom_cbar = {}
cbar_label = {}

trackData = {}


# Define the plot
X_Min=-0.0015000000000000000312250225675825276994
Y_Min=-0.0030486282601243420466163858151276144781
Z_Min=-0.0000007442940088194194449747035681463903
X_Max=0.0045972565202486836283268800684709276538
Y_Max=0.0030486282601243420466163858151276144781
Z_Max=0.0000007442940088194194449747035681463903
MeV=0.0000016021765700000000157555805901932189

dirDiv = '/'
dataFolders = ['Ex2D','Electron2D','Proton2D']
pNames = ['Ex2D','Electron2D','Proton2D','tracks']
tracksFadeFactor = np.sqrt(np.sqrt(0.5))
tracksCutoff = 0.1*MeV
trackSkip = 1

size['Electron2D'] = (1024, 1024)
size['Proton2D'] = (1024, 1024)
size['Ex2D'] = (1024, 1024)

cmap['Electron2D'] = 'GreenBlack'
cmap['Proton2D'] = 'RdPu'
cmap['Ex2D'] = 'seismic'
cmap['tracks'] = 'YlOrRd'

clim['Electron2D'] = (1e4, 1e7)
clim['Proton2D'] = (1e3, 1e5)
clim['Ex2D'] = (-2.5e8, 2.5e8)
clim['tracks'] = (0,5*MeV)

cmapNorm['Electron2D'] = 'logarithmic'
cmapNorm['Proton2D'] = 'logarithmic'
cmapNorm['Ex2D'] = 'linear'
cmapNorm['tracks'] = 'linear'

cbar['Electron2D'] = True
cbar['Proton2D'] = True
cbar['Ex2D'] = True
cbar['tracks'] = True

cbar_label['Electron2D'] = r'Electron Density'
cbar_label['Proton2D'] = r'Proton Density'
cbar_label['Ex2D'] = r'$E_x$'
cbar_label['tracks'] = r'$E_k$ (MeV)'

def Opaque(x): return 1
def Linear(x): return x
def Sqrt(x): return np.sqrt(x)
def LinearSymmetric(x): return np.abs(2*x-1)

alpha['Electron2D'] = Linear
alpha['Proton2D'] = Sqrt
alpha['Ex2D'] = LinearSymmetric
alpha['tracks'] = Opaque

## Create colormaps and data mappings
for pName in pNames:
    ## Create rgba colormap
    # TODO: Safeguard built-in colormaps, unless explicitly overwriting them.
    tc.setAlpha(cmap[pName], alpha[pName])

    ## Create float -> rgba mapping
    if cmapNorm[pName] == 'linear':
        custom_norm[pName] = mpl.colors.Normalize(vmin=clim[pName][0], vmax=clim[pName][1])
    elif cmapNorm[pName] == 'logarithmic':
        custom_norm[pName] = mpl.colors.LogNorm(vmin=clim[pName][0], vmax=clim[pName][1])
    # elif cmapNorm[pName] == 'symlogarithmic'
    #    custom_norm[pName] = mpl.colors.SymLogNorm(vmin=clim[pName][0], vmax=clim[pName][1])
    # elif cmapNorm[pName] == 'power'
    #    custom_norm[pName] = mpl.colors.PowerNorm(vmin=clim[pName][0], vmax=clim[pName][1])
    customDataMapper[pName] = mpl.cm.ScalarMappable(norm=custom_norm[pName], cmap=cmap[pName])

    ## Map rgba cmap -> rgb
    tc.make_alphablended_cmap(cmap[pName], cmap[pName] + "_rgb")
    custom_cbar[pName] = mpl.cm.ScalarMappable(norm=custom_norm[pName], cmap=cmap[pName] + "_rgb")
    custom_cbar[pName].set_array(0)

# Fetch file names
files = sorted([os.path.basename(filename) for filename in glob.glob(dataFolders[0] + dirDiv + '*.bin')])

trackFiles = [os.path.basename(x) for x in glob.glob('ParticleTracking/*.txt')]
for track in trackFiles[::trackSkip]:
    trackData[track] = np.loadtxt('ParticleTracking' + dirDiv + track)

matrixRange = np.array([X_Min,X_Max,Y_Min,Y_Max])
plotExtent = matrixRange/1e-4
x = np.linspace(X_Min/1e-4,X_Max/1e-4,1024)
y = np.linspace(Y_Min/1e-4,Y_Max/1e-4,1024)

def main():
    #pool = multiprocessing.Pool(processes=2)
    #pool.imap_unordered(plot2D, range(len(files)))
    #pool.close()
    #pool.join()

    for i in tqdm(range(len(files))):
        plot2D(i)

t0 = time.time()
main()
print(time.time()-t0)

