import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import TransparentColormaps as tc
import ParticleTracks as pt

from tqdm import tqdm
import time
import multiprocessing


def load_Filenames(Data):
    for dataName in Data:
        if Data[dataName]['type'] == 'tracks':
            Data[dataName]['filenames'] = [os.path.basename(filename) for filename in
                                           glob.glob(Data[dataName]['dir'] + dirDiv + '*.txt')]
        if Data[dataName]['type'] == 'matrix':
            Data[dataName]['filenames'] = sorted([os.path.basename(filename) for filename in glob.glob(Data[dataName]['dir'] + dirDiv + '*.bin')])


def load_data_ParticleTracking(Data):
    for dataName in Data:
        if Data[dataName]['type'] == 'tracks':
            Data[dataName]['data'] = {}
            for track in Data[dataName]['filenames'][::trackSkip]:
                Data[dataName]['data'][track] = np.loadtxt(Data[dataName]['dir'] + dirDiv + track)


def load_data_Matrix(Data, i):
    for dataName in Data:
        if Data[dataName]['type'] == 'matrix':
            Data[dataName]['data'] = (np.fromfile(Data[dataName]['dir'] + dirDiv + Data[dataName]['filenames'][i], dtype='f')).reshape(Data[dataName]['size'])


def create_mappables(pData):
    for pDataName in pData:
        if pData[pDataName]['type'] == 'rgba':
            n = len(pData[pDataName]['input'])
            pData[pDataName]['rgba_mappable'] = [0]*n
            pData[pDataName]['cbar_mappable'] = [0]*n
            for i in range(n):
                ## Create float -> rgba mapping
                if pData[pDataName]['norm'][i] == 'linear':
                    pData[pDataName]['norm'][i] = mpl.colors.Normalize(vmin=pData[pDataName]['clim'][i][0], vmax=pData[pDataName]['clim'][i][1])
                elif pData[pDataName]['norm'][i] == 'logarithmic':
                    pData[pDataName]['norm'][i] = mpl.colors.LogNorm(vmin=pData[pDataName]['clim'][i][0], vmax=pData[pDataName]['clim'][i][1])
                pData[pDataName]['rgba_mappable'][i] = mpl.cm.ScalarMappable(cmap=pData[pDataName]['cmap'][i], norm=pData[pDataName]['norm'][i])

                ## Map rgba cmap -> rgb
                pData[pDataName]['cbar_mappable'][i] = mpl.cm.ScalarMappable(cmap=pData[pDataName]['cmap'][i]+"_rgb", norm=pData[pDataName]['norm'][i])
                pData[pDataName]['cbar_mappable'][i].set_array((0, 1))


def calculate_pData(Data, pData, i):
    for pDataName in pData:
        ## data -> pdata -> rgba -> rgb
        if pData[pDataName]['type'] == 'rgba':
            n = len(pData[pDataName]['input'])
            for idx in range(n):
                dataName = pData[pDataName]['input'][idx]
                if Data[dataName]['type'] == 'matrix':
                    data_RGBA = pData[pDataName]['rgba_mappable'][idx].to_rgba(Data[dataName]['data'])
                elif Data[dataName]['type'] == 'tracks':
                    trackDataMatrix, trackAlpha = pt.getTrackMatrix(Data[dataName]['data'], i, tracksCutoff,
                                                                    matrixRange, tracksFadeFactor)
                    data_RGBA = pData[pDataName]['rgba_mappable'][idx].to_rgba(trackDataMatrix)
                    data_RGBA[..., 3] = trackAlpha
                if idx == 0:
                    background = np.ones(data_RGBA.shape)
                    data_RGB = tc.alphaBlend(data_RGBA, background)
                else:
                    data_RGB = tc.alphaBlend(data_RGBA, data_RGB)
            pData[pDataName]['data'] = data_RGB


def initialize(Data, pData):
    load_Filenames(Data)
    load_data_ParticleTracking(Data)
    create_mappables(pData)


def plot(i):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    fig, ax = plt.subplots(nrows=1)

    load_data_Matrix(Data, i)
    calculate_pData(Data, pData, i)

    for pDataName in pData:
        if pData[pDataName]['type'] == 'rgba':
            ax.imshow(pData[pDataName]['data'], extent=plotExtent, aspect=1, origin='lower')
            n = len(pData[pDataName]['input'])
            for idx in range(n):
                if pData[pDataName]['cbar'][idx]:
                    plt.colorbar(pData[pDataName]['cbar_mappable'][idx], ax=ax, shrink=0.52,
                                 label=pData[pDataName]['cbarLabel'][idx])

    fig.set_tight_layout(True)
    ax.set_xlabel(r'$x$ ($\mu$m)')
    ax.set_ylabel(r'$y$ ($\mu$m)')
    ax.set_title("Frame " + str(i))
    fig.canvas.draw()
    fig.savefig(os.path.splitext(Data['Ex']['filenames'][i])[0] + '.png', dpi=300)
    # TODO: Fix the file naming and an output dictionary.
    plt.close()


######################################################################
######################################################################

## Create Colormaps
def Opaque(x): return 1
def Linear(x): return x
def Sqrt(x): return np.sqrt(x)
def LinearSymmetric(x): return np.abs(2*x-1)

tc.make_rgb_colormap("GreenBlack", ['g', 0.75, 'g', 'k'])
tc.setAlpha("GreenBlack", Linear)
tc.make_alphablended_cmap("GreenBlack", "GreenBlack_rgb")

tc.setAlpha("RdPu", Sqrt)
tc.make_alphablended_cmap("RdPu", "RdPu_rgb")

tc.setAlpha("seismic", LinearSymmetric)
tc.make_alphablended_cmap("seismic", "seismic_rgb")

tc.make_alphablended_cmap("YlOrRd", "YlOrRd_rgb")
# TODO: Safeguard built-in colormaps, unless explicitly overwriting them.
# TODO: Automate creation (and use of) alphablended cmaps for colorbars.


dirDiv = '/'
X_Min = -0.0015000000000000000312250225675825276994
Y_Min = -0.0030486282601243420466163858151276144781
Z_Min = -0.0000007442940088194194449747035681463903
X_Max = 0.0045972565202486836283268800684709276538
Y_Max = 0.0030486282601243420466163858151276144781
Z_Max = 0.0000007442940088194194449747035681463903
MeV = 0.0000016021765700000000157555805901932189

trackSkip = 1
tracksFadeFactor = np.sqrt(np.sqrt(0.5))
tracksCutoff = 0.1*MeV
matrixRange = np.array([X_Min,X_Max,Y_Min,Y_Max])
plotExtent = np.array([X_Min,X_Max,Y_Min,Y_Max])/1e-4


Data = {}

Data['Ex'] = {}
Data['Ex']['dir'] = 'Ex2D'
Data['Ex']['type'] = 'matrix'
Data['Ex']['size'] = (1024, 1024)
#Data['Ex']['dim'] = ('x', 'y')
#Data['Ex']['coords'] = [np.linspace(X_Min,X_Max,1024), np.linspace(Y_Min,Y_Max,1024)]

Data['Ne'] = {}
Data['Ne']['dir'] = 'Electron2D'
Data['Ne']['type'] = 'matrix'
Data['Ne']['size'] = (1024, 1024)
#Data['Ne']['dim'] = ('x', 'y')
#Data['Ne']['coords'] = [np.linspace(X_Min,X_Max,1024), np.linspace(Y_Min,Y_Max,1024)]

Data['Np'] = {}
Data['Np']['dir'] = 'Proton2D'
Data['Np']['type'] = 'matrix'
Data['Np']['size'] = (1024, 1024)
#Data['Np']['dim'] = ('x', 'y')
#Data['Np']['coords'] = [np.linspace(X_Min,X_Max,1024), np.linspace(Y_Min,Y_Max,1024)]

Data['ElectronTracks'] = {}
Data['ElectronTracks']['dir'] = 'ParticleTracking'
Data['ElectronTracks']['type'] = 'tracks'
#Data['ElectronTracks']['dim'] = ['x', 'y', 'z', 'px', 'py', 'pz', 'E']
# TODO: Set default values for e.g. 'dir'.
# TODO: Make use of 'dim' and 'coords'.


pData = {}

pData['XY'] = {}
pData['XY']['type'] = 'rgba'
pData['XY']['input'] = ['Ex', 'Ne', 'Np', 'ElectronTracks']
pData['XY']['cmap'] = ['seismic', 'GreenBlack', 'RdPu', 'YlOrRd']
pData['XY']['clim'] = [(-2.5e8, 2.5e8), (1e4, 1e7), (1e3, 1e5), (0,5*MeV)]
pData['XY']['norm'] = ['linear', 'logarithmic', 'logarithmic', 'linear']
pData['XY']['cbar'] = [True, True, True, True]
pData['XY']['cbarLabel'] = [r'$E_x$', r'Electron Density', r'Proton Density', r'$E_k$ (MeV)']


initialize(Data, pData)
for i in tqdm(range(len(Data['Ex']['filenames']))):
    plot(i)

# TODO: Split Data and pData such that multiprocessing will can be re-instated.
#pool = multiprocessing.Pool(processes=2)
#pool.imap_unordered(plot2D, range(len(files)))
#pool.close()
#pool.join()
