import matplotlib as mpl
import transparentcolormaps as tc
import numpy as np


def calculate_dependables(axesSettings, plotSettings):
    for settings in plotSettings:
        for axisSettings in axesSettings:
            if axisSettings['name'] == settings['ax']:
                axSettings = axisSettings
        calculateDependables(axSettings, settings)


def calculateDependables(axisSettings, plotSettings):
    # Get axis rescaling factors
    if 'cbarunits_value' not in plotSettings.keys():
        plotSettings.add_value('cbarunits_value', 1)
    for dim in ['x', 'y']:
        key = dim + 'units_value'
        plotSettings.add_value(key, 1)
        if key in axisSettings.keys():
            plotSettings.add_value(key, axisSettings[key])

    if plotSettings['plot_type'] == 'rgba':
        # Rescale extent according to units
        plotExtent = np.array([plotSettings['xMin'], plotSettings['xMax'], plotSettings['yMin'], plotSettings['yMax']])
        plotExtent[:2] = plotExtent[:2] / plotSettings['xunits_value']
        plotExtent[2:] = plotExtent[2:] / plotSettings['yunits_value']
        plotSettings.add_value('plotExtent', plotExtent)

        if plotSettings['data_type'] == 'float':
            # norm
            norm = mpl.colors.Normalize(vmin=plotSettings['clim'][0], vmax=plotSettings['clim'][1])
            cbar_norm = mpl.colors.Normalize(vmin=plotSettings['clim'][0]/plotSettings['cbarunits_value'],
                                             vmax=plotSettings['clim'][1]/plotSettings['cbarunits_value'])
            if 'norm' in plotSettings.keys():
                if plotSettings['norm'] == 'logarithmic':
                    norm = mpl.colors.LogNorm(vmin=plotSettings['clim'][0], vmax=plotSettings['clim'][1])
                    cbar_norm = mpl.colors.LogNorm(vmin=plotSettings['clim'][0] / plotSettings['cbarunits_value'],
                                                   vmax=plotSettings['clim'][1] / plotSettings['cbarunits_value'])

            plotSettings.add_value('norm', norm)
            plotSettings.add_value('cbar_norm', cbar_norm)

            # cmap
            tc.make_alphablended_cmap(plotSettings['cmap'], 'cbar_'+plotSettings['cmap'])

            # mappable
            mappable = mpl.cm.ScalarMappable()
            mappable.set_array((0, 1))
            mappable.set_cmap(plotSettings['cmap'])
            mappable.set_norm(plotSettings['norm'])
            plotSettings.add_value('mappable', mappable)

            cbar_mappable = mpl.cm.ScalarMappable()
            cbar_mappable.set_array((0, 1))
            cbar_mappable.set_cmap('cbar_'+plotSettings['cmap'])
            cbar_mappable.set_norm(plotSettings['cbar_norm'])
            plotSettings.add_value('cbar_mappable', cbar_mappable)
