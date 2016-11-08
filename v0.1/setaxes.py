import matplotlib.ticker as ticker


def setAxes(axes, axesSettings):
    for axisSettings in axesSettings:
        ax = axes[axisSettings['name']]
        setAxis(ax, axisSettings)


def setAxis(ax, axisSettings):

    if axisSettings is not None:
        for key, value in axisSettings.items():
            if key == 'title':
                ax.set_title(value)
            if key == 'aspect':
                ax.set_aspect(value)
            if key == 'xlabel':
                ax.set_xlabel(value)
            if key == 'xlim':
                ax.set_xlim(value)
            if key == 'xscale':
                ax.set_xscale(value)
            if key == 'visible_xticks':
                if not value:
                    ax.set_xticklabels([])
            if key == 'xlabel_top':
                if value:
                    ax.tick_params(axis='x', which='both', labelbottom='off', labeltop='on')
                    ax.xaxis.set_label_position('top')
            if key == 'xticks_out':
                if value:
                    ax.get_xaxis().set_tick_params(which='both', direction='out')
            if key == 'ylabel':
                ax.set_ylabel(value)
            if key == 'ylim':
                ax.set_ylim(value)
            if key == 'yscale':
                ax.set_yscale(value)
            if key == 'visible_yticks':
                if not value:
                    ax.set_yticklabels([])
            if key == 'ylabel_right':
                if value:
                    ax.tick_params(axis='y', which='both', labelleft='off', labelright='on')
                    ax.yaxis.set_label_position('right')
            if key == 'yticks_out':
                if value:
                    ax.get_yaxis().set_tick_params(which='both', direction='out')

    if 'xunits_value' in axisSettings.keys():
        xticks = ticker.FuncFormatter(lambda x, pos: '${0:g}$'.format(x/axisSettings['xunits_value']))
        ax.xaxis.set_major_formatter(xticks)
    if 'yunits_value' in axisSettings.keys():
        yticks = ticker.FuncFormatter(lambda x, pos: '${0:g}$'.format(x/axisSettings['yunits_value']))
        ax.yaxis.set_major_formatter(yticks)
