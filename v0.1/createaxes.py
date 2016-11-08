import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


def createAxes(axesSettings):
    axes = {}
    for axisSettings in axesSettings:
        axes[axisSettings['name']] = createAxis(axes, axisSettings)
    return axes


def createAxis(axes, axisSettings):
    ax = initializeAxis(axes, axisSettings)
    return ax


def initializeAxis(axes, axisSettings):
    subplot2grid_required = ['shape', 'loc']
    subplot2grid_optional = ['rowspan', 'colspan']

    axes_required = ['position']
    axes_optional = []

    zoomed_inset_required = ['parent_axes', 'zoom']
    zoomed_inset_optional = ['loc']

    mark_inset_required = ['parent_axes', 'loc1', 'loc2']
    mark_inset_optional = ['ec']

    # subplot2grid
    if set(subplot2grid_required).issubset(set(axisSettings.keys())):
        kwargs = {}
        for key, value in axisSettings.items():
            if key in subplot2grid_required or key in subplot2grid_optional:
                kwargs[key] = value
        ax = plt.subplot2grid(**kwargs)
        plt.tight_layout()
        return ax

    # axes
    elif set(axes_required).issubset(set(axisSettings.keys())):
        kwargs = {}
        for key, value in axisSettings.items():
            if key in axes_optional:
                kwargs[key] = value
        ax = plt.axes(axisSettings[axes_required[0]], **kwargs)
        return ax

    # zoomed_inset_axes
    elif set(zoomed_inset_required).issubset(set(axisSettings.keys())):
        kwargs = {}
        marked_kwargs = {}
        for key, value in axisSettings.items():
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
        if set(mark_inset_required).issubset(set(axisSettings.keys())):
            mark_inset(inset_axes=ax, fc='none', **marked_kwargs)
        return ax
