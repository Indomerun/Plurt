import matplotlib as mpl


def calculate_dependables(axesSettings, plotSettings):
    for settings in plotSettings:
        for axisSettings in axesSettings:
            if axisSettings['name'] == settings['ax']:
                settings.add_value('axisSettings', axisSettings)
        calculateDependables(settings)


def calculateDependables(plotSettings):

    if plotSettings['plot_type'] == 'rgba' and plotSettings['data_type'] == 'float':
        # norm
        norm = mpl.colors.Normalize(vmin=plotSettings['clim'][0], vmax=plotSettings['clim'][1])
        if 'norm' in plotSettings.keys():
            if plotSettings['norm'] == 'logarithmic':
                norm = mpl.colors.LogNorm(vmin=plotSettings['clim'][0], vmax=plotSettings['clim'][1])
        plotSettings.add_value('norm', norm)

        # mappable
        mappable = mpl.cm.ScalarMappable()
        mappable.set_array((0, 1))
        mappable.set_cmap(plotSettings['cmap'])
        mappable.set_norm(plotSettings['norm'])
        plotSettings.add_value('mappable', mappable)

        #cmap


