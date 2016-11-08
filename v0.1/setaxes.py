
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
                xlim = value
                if 'xunits_value' in axisSettings.keys():
                    xlim = [xlim[0]/axisSettings['xunits_value'], xlim[1]/axisSettings['xunits_value']]
                ax.set_xlim(xlim)
            if key == 'xscale':
                ax.set_xscale(value)
            if key == 'ylabel':
                ax.set_ylabel(value)
            if key == 'ylim':
                ylim = value
                if 'yunits_value' in axisSettings.keys():
                    ylim = [ylim[0]/axisSettings['yunits_value'], ylim[1]/axisSettings['yunits_value']]
                ax.set_ylim(ylim)
            if key == 'yscale':
                ax.set_yscale(value)

            if key == 'hide_axis' and value is True:
                ax.set_axis_off()
            if key == 'hide_ticks' and value is True:
                ax.xaxis.set_tick_params(which='both', bottom='off', top='off')
                ax.yaxis.set_tick_params(which='both', left='off', right='off')
            if key == 'hide_border' and value is True:
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                ax.spines['left'].set_visible(False)
            if key == 'hide_ticklabels':
                if value == 'x' or value == 'both':
                    ax.set_xticklabels([])
                if value == 'y' or value == 'both':
                    ax.set_yticklabels([])
            if key == 'ticks_out':
                if value == 'x' or value == 'both':
                    ax.xaxis.set_tick_params(which='both', direction='out')
                if value == 'y' or value == 'both':
                    ax.yaxis.set_tick_params(which='both', direction='out')
            if key == 'hide_xticks':
                if value == 'bottom' or value == 'both':
                    ax.xaxis.set_tick_params(which='both', bottom='off')
                if value == 'top' or value == 'both':
                    ax.xaxis.set_tick_params(which='both', top='off')
            if key == 'hide_xborder':
                if value == 'bottom' or value == 'both':
                    ax.spines['bottom'].set_visible(False)
                if value == 'top' or value == 'both':
                    ax.spines['top'].set_visible(False)
            if key == 'xlabel_top':
                if value:
                    ax.tick_params(axis='x', which='both', labelbottom='off', labeltop='on')
                    ax.xaxis.set_label_position('top')
            if key == 'hide_yticks':
                if value == 'left' or value == 'both':
                    ax.yaxis.set_tick_params(which='both', left='off')
                if value == 'right' or value == 'both':
                    ax.yaxis.set_tick_params(which='both', right='off')
            if key == 'hide_yborder':
                if value == 'left' or value == 'both':
                    ax.spines['left'].set_visible(False)
                if value == 'right' or value == 'both':
                    ax.spines['right'].set_visible(False)
            if key == 'ylabel_right':
                if value:
                    ax.tick_params(axis='y', which='both', labelleft='off', labelright='on')
                    ax.yaxis.set_label_position('right')

