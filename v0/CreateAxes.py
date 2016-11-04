import matplotlib.pyplot as plt
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


def setAxes(ax, axesSettings):
    if axesSettings is not None:
        for key, value in axesSettings.items():
            if key == 'title':
                ax.set_title(value)
            if key == 'xlabel':
                ax.set_xlabel(value)
            if key == 'xlim':
                ax.set_xlim(value)
            if key == 'xscale':
                ax.set_xscale(value)
            if key == 'visible_xticks':
                plt.xticks(visible=value)
                #if not value:
                #    ax.set_xticklabels([])
            if key == 'xlabel_top':
                if value:
                    ax.tick_params(axis='x', which='both', labelbottom='off', labeltop='on')
                    ax.xaxis.set_label_position('top')
            if key == 'ylabel':
                ax.set_ylabel(value)
            if key == 'ylim':
                ax.set_ylim(value)
            if key == 'yscale':
                ax.set_yscale(value)
            if key == 'visible_yticks':
                plt.yticks(visible=value)
                #if not value:
                #    ax.set_yticklabels([])
            if key == 'ylabel_right':
                if value:
                    ax.tick_params(axis='y', which='both', labelleft='off', labelright='on')
                    ax.yaxis.set_label_position('right')


def createAxes(axes, axesSettings):
    ax = initializeAxes(axes, axesSettings)
    setAxes(ax, axesSettings)
    return ax


def getAxes(axesSettings):
    axes = {}
    for settings in axesSettings:
        axes[settings['name']] = createAxes(axes, settings)
    return axes

