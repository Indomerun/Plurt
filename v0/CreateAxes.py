import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


def initializeAxes(axes, axesSettings):
    subplot2grid_required = ['shape', 'loc']
    subplot2grid_optional = ['rowspan', 'colspan']

    axes_required = ['position']
    axes_optional = []

    zoomed_inset_required = ['parent_axes', 'zoom']
    zoomed_inset_optional = ['loc']

    mark_inset_required = ['parent_axes', 'loc1', 'loc2']
    mark_inset_optional = ['ec']

    if set(subplot2grid_required).issubset(set(axesSettings.keys())):
        kwargs = {}
        for key, value in axesSettings.items():
            if key in subplot2grid_required or key in subplot2grid_optional:
                kwargs[key] = value
        ax = plt.subplot2grid(**kwargs)
        plt.tight_layout()
        return ax

    elif set(axes_required).issubset(set(axesSettings.keys())):
        kwargs = {}
        for key, value in axesSettings.items():
            if key in axes_optional:
                kwargs[key] = value
        ax = plt.axes(axesSettings[axes_required[0]], **kwargs)
        return ax

    elif set(zoomed_inset_required).issubset(set(axesSettings.keys())):
        kwargs = {}
        marked_kwargs = {}
        for key, value in axesSettings.items():
            if key in zoomed_inset_required or key in zoomed_inset_optional:
                if key == 'parent_axes':
                    kwargs[key] = axes[value]
                else:
                    kwargs[key] = value
            if key in mark_inset_required or key in mark_inset_optional:
                if key == 'parent_axes':
                    marked_kwargs[key] = axes[value]
                else:
                    marked_kwargs[key] = value
        ax = zoomed_inset_axes(**kwargs)
        if set(mark_inset_required).issubset(set(axesSettings.keys())):
            mark_inset(inset_axes=ax, fc='none', **marked_kwargs)
        return ax


def get_label(dim, axesSettings):
    label = []
    if dim + 'label' in axesSettings.keys():
        label.append(axesSettings[dim + 'label'])
    if dim + 'units' in axesSettings.keys():
        label.append('[' + axesSettings[dim + 'units'] + ']')
    if label != []:
        return ' '.join(label)


def setAxis(ax, axesSettings):
    xlabel = get_label('x', axesSettings)
    ylabel = get_label('y', axesSettings)

    if axesSettings is not None:
        for key, value in axesSettings.items():
            if key == 'title':
                ax.set_title(value)
            if key == 'aspect':
                ax.set_aspect(value)
            if xlabel is not None:
                ax.set_xlabel(xlabel)
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
            if ylabel is not None:
                ax.set_ylabel(ylabel)
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

    if 'xunits_value' in axesSettings.keys():
        xticks = ticker.FuncFormatter(lambda x, pos: '${0:g}$'.format(x/axesSettings['xunits_value']))
        ax.xaxis.set_major_formatter(xticks)
    if 'yunits_value' in axesSettings.keys():
        yticks = ticker.FuncFormatter(lambda x, pos: '${0:g}$'.format(x/axesSettings['yunits_value']))
        ax.yaxis.set_major_formatter(yticks)


def setAxes(axes, axesSettings):
    for settings in axesSettings:
        ax = axes[settings['name']]
        setAxis(ax, settings)


def createAxes(axes, axesSettings):
    ax = initializeAxes(axes, axesSettings)
    return ax


def getAxes(axesSettings):
    axes = {}
    for settings in axesSettings:
        axes[settings['name']] = createAxes(axes, settings)
    return axes
