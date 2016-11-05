import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import TransparentColormaps as tc
import CreateAxes as ca
import os


def getDependableSettings(plotSettings):
    dependableSettings = {}

    if plotSettings['plot_type'] == 'rgba' and plotSettings['data_type'] == 'float':
        if plotSettings['norm'] == 'linear':
            dependableSettings['norm'] = mpl.colors.Normalize(vmin=plotSettings['clim'][0], vmax=plotSettings['clim'][1])
        elif plotSettings['norm'] == 'logarithmic':
            dependableSettings['norm'] = mpl.colors.LogNorm(vmin=plotSettings['clim'][0], vmax=plotSettings['clim'][1])

        dependableSettings['mappable'] = mpl.cm.ScalarMappable()
        dependableSettings['mappable'].set_array((0, 1))
        dependableSettings['mappable'].set_cmap(plotSettings['cmap'])
        dependableSettings['mappable'].set_norm(dependableSettings['norm'])
    return dependableSettings


def getDependables(plotSettings):
    nPlots = len(plotSettings)
    dependableSettings = [{}]*nPlots
    for i in range(nPlots):
        dependableSettings[i] = getDependableSettings(plotSettings[i])
    return dependableSettings


def import_data(plotSettings, frameNumber):
    if plotSettings['data_type'] == 'float':
        fileName = ("%06d" % frameNumber) + '.bin'
        data = (np.fromfile(plotSettings['name'] + os.path.sep + fileName, dtype='f')).reshape(plotSettings['size'])
        return data
    if plotSettings['data_type'] == 'bmp':
        img = Image.open('../Canada-Flag.bmp')
        return np.asarray(img)
    if plotSettings['data_type'] == 'line':
        x = np.linspace(plotSettings['xMin'], plotSettings['xMax'], plotSettings['size'])
        data = np.array([x, np.sin(x)])
        return data


def fetch_data(plotSettings, loadedData, frameNumber):
    if plotSettings['name'] in loadedData.keys():
        data = loadedData[plotSettings['name']]
    else:
        data = import_data(plotSettings, frameNumber)
        loadedData[plotSettings['name']] = data
    return data


def plot_rgba(axes, data, plotSettings, dependableSettings):
    plotExtent = [plotSettings['xMin'], plotSettings['xMax'], plotSettings['yMin'], plotSettings['yMax']]
    if plotSettings['data_type'] == 'float':
        data_RGBA = dependableSettings['mappable'].to_rgba(data)
    elif plotSettings['data_type'] == 'bmp':
        data_RGBA = np.ones(data.shape)
        data_RGBA[..., :3] = np.flipud(data)/255
    ax = axes[plotSettings['ax']]
    im = ax.get_images()
    if len(im) == 0:
        ax.imshow(data_RGBA, extent=plotExtent, origin='lower', aspect='auto')
    elif len(im) == 1:
        imdata = im[0].get_array()
        blendedData = tc.alphaBlend(data_RGBA, imdata)
        im[0].set_data(blendedData)


def plot_cbar(axes, plotSettings, dependableSettings):
    if 'cax' in plotSettings.keys():
        cbar = plt.colorbar(dependableSettings['mappable'], cax=axes[plotSettings['cax']])
    else:
        cbar = plt.colorbar(dependableSettings['mappable'], ax=axes[plotSettings['ax']])
    label = ca.get_label('cbar', plotSettings)
    if label is not None:
        cbar.set_label(label)


def plot_line(axes, data, plotSettings, dependableSettings):
    ax = axes[plotSettings['ax']]
    ax.plot(data[0, :], data[1, :])


def add_plot(axes, plotSettings, dependableSettings, loadedData, frameNumber):
    data = fetch_data(plotSettings, loadedData, frameNumber)
    if plotSettings['plot_type'] == 'rgba':
        plot_rgba(axes, data, plotSettings, dependableSettings)
        if 'show_cbar' in plotSettings.keys() and plotSettings['show_cbar']:
            plot_cbar(axes, plotSettings, dependableSettings)
    elif plotSettings['plot_type'] == 'line':
        plot_line(axes, data, plotSettings, dependableSettings)


def add_plots(axes, plotSettings, dependableSettings, frameNumber):
    loadedData = {}
    nPlots = len(plotSettings)
    for i in range(nPlots):
        add_plot(axes, plotSettings[i], dependableSettings[i], loadedData, frameNumber)


# TODO: Add ParticleTracks
# TODO: Add multiprocessing
# TODO: Implement alternative "alpha"-blending
# TODO: Add 'zorder' for manual control of what will be on top
# TODO: Option for hiding the bbox, ticks, tick labels and labels
# TODO: Move get_label to a new file for auxilary functions
# TODO: Rescale cbar ticks with units
