import auxilaries as aux


class MappableSettings(object):
    _default_mappings = {}

    def __init__(self, settings=None):
        if settings is None:
            self._settings = {}
        else:
            self._settings = settings.copy()

        self._mappings = self._default_mappings
        self._is_mapped = False

    def set_settings(self, settings):
        self._settings = settings.copy()
        self._is_mapped = False

    def set_mappings(self, mappings):
        self._mappings = mappings.copy()
        self._is_mapped = False

    def map_settings(self):
        self._mapped_settings = {}
        for key, value in self._mappings.items():
            try:
                if type(value) == str:
                    if value == '':
                        self._mapped_settings[key] = self._settings[key]
                    else:
                        self._mapped_settings[key] = self._settings[value]
                else:
                    self._mapped_settings[key] = value(self._settings)
            except KeyError:
                pass
        self._is_mapped = True

    def __getitem__(self, key):
        return self._mapped_settings[key]

    def keys(self):
        return self._mapped_settings.keys()

    def values(self):
        return self._mapped_settings.values()

    def items(self):
        return self._mapped_settings.items()

    def add_dependencies(self, dependencies):
        for key, value in dependencies.items():
            self._mapped_settings[key] = value

    def add_value(self, key, value):
        self._mapped_settings[key] = value



class FigureSettings(MappableSettings):
    _default_mappings = dict(name='',
                             pixels='')


class AxisSettings(MappableSettings):
    _default_mappings = dict(name='',

                             # subplot2grid
                             shape=lambda x: [x['nrows'], x['ncols']],
                             loc=lambda x: [x['row'], x['col']] if ('row' in x.keys() and 'col' in x.keys()) else x['inset_position'],
                             rowspan='',
                             colspan='',

                             # axes
                             position=lambda x: [x['position'][0], x['position'][1], x['position'][2]-x['position'][0], x['position'][3]-x['position'][1]],

                             # zoomed_inset_axes
                             parent_axes='parent_axis',
                             zoom='inset_zoom',
                             #loc='inset_position',

                             # mark_inset
                             #parent_axes='parent_axis',
                             loc1='corner1',
                             loc2='corner2',
                             ec='color',

                             # Other settings
                             title='',
                             aspect='',
                             xlabel=lambda x: aux.get_label(x, 'xlabel', 'xunits'),
                             xunits_value='',
                             xlim='',
                             xscale='',
                             ylabel=lambda x: aux.get_label(x, 'ylabel', 'yunits'),
                             yunits_value='',
                             ylim='',
                             yscale='',
                             hide_axis='',                      # True or False
                             hide_ticks='',                     # True or False
                             hide_border='',                    # True or False
                             hide_ticklabels='',                # 'x', 'y' or 'both'
                             ticks_out='',                      # 'x', 'y' or 'both'
                             hide_xticks='',                    # 'top', 'bottom', or 'both'
                             hide_xborder='',                   # 'top', 'bottom', or 'both'
                             xlabel_top='',                     # True or False
                             hide_yticks='',                    # 'left', 'right', or 'both'
                             hide_yborder='',                   # 'left', 'right', or 'both'
                             ylabel_right='',                   # True or False
                             )


class PlotSettings(MappableSettings):
    _default_mappings = dict(name='',

                             # Required
                             ax='',
                             plot_type='',
                             data_type='',
                             size='',

                             # plot_type = rgba
                             xMin='',
                             xMax='',
                             yMin='',
                             yMax='',
                             cmap='',
                             clim='',
                             norm='',
                             show_cbar='',
                             cbarlabel=lambda x: aux.get_label(x, 'cbarlabel', 'cbarunits'),
                             cbarunits_value='',
                             cax='',
                             )
