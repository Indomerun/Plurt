import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from tqdm import tqdm
#from matplotlib.collections import LineCollection

from matplotlib.image import NonUniformImage

def bresenham(x,y,x2,y2):
    """Brensenham line algorithm"""
    steep = 0
    coords = []
    dx = abs(x2 - x)
    if (x2 - x) > 0: sx = 1
    else: sx = -1
    dy = abs(y2 - y)
    if (y2 - y) > 0: sy = 1
    else: sy = -1
    if dy > dx:
        steep = 1
        x,y = y,x
        dx,dy = dy,dx
        sx,sy = sy,sx
    d = (2 * dy) - dx
    for i in range(0,dx):
        if steep: coords.append((y,x))
        else: coords.append((x,y))
        while d >= 0:
            y = y + sy
            d = d - (2 * dx)
        x = x + sx
        d = d + (2 * dy)
    return coords

def initializeTrackMatrix(i,trackData,tracksCutoff):
    trackDataMatrix = np.zeros((1024, 1024))
    trackAlpha = np.zeros((1024, 1024))
    for track in trackData:
        if (trackData[track].shape[0] > i) and (trackData[track][i, 6] > tracksCutoff):
            currentBin = (int(1024 * (trackData[track][i, 1] - Y_Min) / (Y_Max - Y_Min)),
                          int(1024 * (trackData[track][i, 0] - X_Min) / (X_Max - X_Min)))
            trackDataMatrix[currentBin] = trackData[track][i, 6] / MeV
            trackAlpha[currentBin] = 1
    return trackDataMatrix, trackAlpha

def updateTrackMatrix(i,trackData,trackDataMatrix,trackAlpha,tracksFadeFactor,tracksCutoff):
    trackAlpha *= tracksFadeFactor
    for track in trackData:
        if (trackData[track].shape[0] > i) and (trackData[track][i, 6] > tracksCutoff):
            previousBin = (int(1024 * (trackData[track][i - 1, 1] - Y_Min) / (Y_Max - Y_Min)),
                           int(1024 * (trackData[track][i - 1, 0] - X_Min) / (X_Max - X_Min)))
            currentBin = (int(1024 * (trackData[track][i, 1] - Y_Min) / (Y_Max - Y_Min)),
                          int(1024 * (trackData[track][i, 0] - X_Min) / (X_Max - X_Min)))

            Bins = bresenham(previousBin[0], previousBin[1], currentBin[0], currentBin[1])
            for bin in Bins:
                trackDataMatrix[bin] = trackData[track][i, 6] / MeV
                trackAlpha[bin] = 1
            trackDataMatrix[currentBin] = trackData[track][i, 6] / MeV
            trackAlpha[currentBin] = 1

def getTrackMatrix(i,trackData,tracksFadeFactor,tracksCutoff):
    trackDataMatrix, trackAlpha = initializeTrackMatrix(i, trackData, tracksCutoff)
    for j in range(max(0,i-32),i+1):
        updateTrackMatrix(j, trackData, trackDataMatrix, trackAlpha, tracksFadeFactor, tracksCutoff)
    return trackDataMatrix, trackAlpha

# Return a copy of the cmap
def getCMapCopy(cmapName):
    cmapBase = mpl.cm.get_cmap(cmapName)
    color_list = cmapBase(np.linspace(0, 1, cmapBase.N))
    new_cmapName = None
    return cmapBase.from_list(new_cmapName, color_list)

def make_colormap(name, seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [mpl.colors.colorConverter.to_rgb(element) if isinstance(element, str) else element for element in seq]
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])

    mpl.cm.register_cmap(name, mpl.colors.LinearSegmentedColormap('CustomMap', cdict))

# Create custom transparency for a colormap.
# aFun is assumed to be defined on the interval [0,1]
def setAlpha(cmap,aFun=None):
    cmap._init()
    if aFun is None:
        return
    alpha = aFun(np.linspace(0, 1, cmap.N))
    cmap._lut[:-3, -1] = alpha
    cmap._lut[-3, -1] = cmap._lut[0, -1]
    cmap._lut[-2, -1] = cmap._lut[-4, -1]

def alphaBlend(src_RGBA, dst_RGBA):
    src_A = src_RGBA[..., -1]
    src_R = src_RGBA[..., 0]
    src_G = src_RGBA[..., 1]
    src_B = src_RGBA[..., 2]
    dst_A = dst_RGBA[..., -1]
    dst_R = dst_RGBA[..., 0]
    dst_G = dst_RGBA[..., 1]
    dst_B = dst_RGBA[..., 2]

    """ # Allow transparent dst
    out_A = src_A + dst_A * (1 - src_A)
    out_R = (src_R * src_A + dst_R * dst_A * (1 - src_A)) / out_A
    out_G = (src_G * src_A + dst_G * dst_A * (1 - src_A)) / out_A
    out_B = (src_B * src_A + dst_B * dst_A * (1 - src_A)) / out_A
    """

    # Force opaque dst
    out_A = np.ones(dst_A.shape)
    out_R = dst_R + (src_R - dst_R) * src_A
    out_G = dst_G + (src_G - dst_G) * src_A
    out_B = dst_B + (src_B - dst_B) * src_A

    out_RGBA = np.zeros(src_RGBA.shape)
    out_RGBA[..., -1] = out_A
    out_RGBA[..., 0] = out_R
    out_RGBA[..., 1] = out_G
    out_RGBA[..., 2] = out_B

    return out_RGBA

def getAlphaBlendedCMap(cmapName):
    cmapBase = mpl.cm.get_cmap(cmapName)
    src_RGBA = cmapBase(np.linspace(0, 1, cmapBase.N))
    dst_RGBA = np.ones(src_RGBA.shape)
    new_cmapName = None
    return cmapBase.from_list(new_cmapName, alphaBlend(src_RGBA, dst_RGBA))

# Create new colormaps
make_colormap("GreenBlack", ['g', 0.75, 'g', 'k'])
make_colormap("RedBlack", ['r', 0.75, 'r', 'k'])

# Declare structs
size = {}
pData = {}
cmap = {}
clim = {}
cmapNorm = {}
cbar = {}
alpha = {}

data = {}
custom_cmap = {}
custom_norm = {}
customDataMapper = {}
data_RGBA = {}
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
clim['tracks'] = (0,5)

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
for pName in pNames+['tracks']:
    ## Create rgba colormap
    custom_cmap[pName] = getCMapCopy(cmap[pName])
    setAlpha(custom_cmap[pName], alpha[pName])
    mpl.cm.register_cmap(pName + "_alpha", custom_cmap[pName])

    ## Create float -> rgba mapping
    if cmapNorm[pName] == 'linear':
        custom_norm[pName] = mpl.colors.Normalize(vmin=clim[pName][0], vmax=clim[pName][1])
    elif cmapNorm[pName] == 'logarithmic':
        custom_norm[pName] = mpl.colors.LogNorm(vmin=clim[pName][0], vmax=clim[pName][1])
    # elif cmapNorm[pName] == 'symlogarithmic'
    #    custom_norm[pName] = mpl.colors.SymLogNorm(vmin=clim[pName][0], vmax=clim[pName][1])
    # elif cmapNorm[pName] == 'power'
    #    custom_norm[pName] = mpl.colors.PowerNorm(vmin=clim[pName][0], vmax=clim[pName][1])
    customDataMapper[pName] = mpl.cm.ScalarMappable(norm=custom_norm[pName], cmap=(pName + "_alpha"))

    ## Map rgba cmap -> rgb
    custom_cmap[pName] = getAlphaBlendedCMap(pName + "_alpha")
    mpl.cm.register_cmap(pName + "_alpha_blended", custom_cmap[pName])
    custom_cbar[pName] = mpl.cm.ScalarMappable(norm=custom_norm[pName], cmap=(pName + "_alpha_blended"))
    custom_cbar[pName].set_array(0)


# Fetch file names
files = sorted([os.path.basename(filename) for filename in glob.glob(dataFolders[0] + dirDiv + '*.bin')])

trackFiles = [os.path.basename(x) for x in glob.glob('ParticleTracking/*.txt')]
for track in trackFiles[::trackSkip]:
    trackData[track] = np.loadtxt('ParticleTracking' + dirDiv + track)

# Declare the figure
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fig, ax = plt.subplots(nrows=1)

plotExtent = [X_Min/1e-4,X_Max/1e-4,Y_Min/1e-4,Y_Max/1e-4]
x = np.linspace(X_Min/1e-4,X_Max/1e-4,1024)
y = np.linspace(Y_Min/1e-4,Y_Max/1e-4,1024)

for i in tqdm(range(len(files))):
    ## load data
    for folder in dataFolders:
        Current_filename = files[i]
        data[folder] = (np.fromfile(folder + dirDiv + Current_filename, dtype='f')).reshape(size[folder])

    ## data -> pdata -> rgba -> rgb
    for idx, pName in enumerate(pNames):
        if pName == 'tracks':
            trackDataMatrix, trackAlpha = getTrackMatrix(i, trackData, tracksFadeFactor, tracksCutoff)
            pData[pName] = trackDataMatrix
        else:
            pData[pName] = data[pName]

        data_RGBA[pName] = customDataMapper[pName].to_rgba(pData[pName])
        if pName == 'tracks':
            data_RGBA[pName][..., 3] = trackAlpha

        if idx == 0:
            background = np.ones(data_RGBA[pName].shape)
            data_RGB = alphaBlend(data_RGBA[pName], background)
        else:
            data_RGB = alphaBlend(data_RGBA[pName], data_RGB)

    # Plot rgb data
    if i == 0:
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


    else:
        im.set_data(x, y, data_RGB)
        #for track in trackFiles[::trackSkip]:
        #    points = np.array([trackData[track][max(0,i-10):i+1, 0] / 1e-4, trackData[track][max(0,i-10):i+1, 1] / 1e-4]).T.reshape(-1, 1, 2)
        #    segments = np.concatenate([points[:-1], points[1:]], axis=1)
        #    trackax[track].set_segments(segments)
        #    trackax[track].set_array(trackData[track][max(0,i-10):i+1, 6] / MeV)


    ax.set_title("Frame " + str(i))
    fig = plt.gcf()
    #fig.show()
    fig.canvas.draw()
    fig.savefig(os.path.splitext(Current_filename)[0] + '.png', dpi=300)


