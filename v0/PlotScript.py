import Plot as plot


# --- Constants from Input --- #
X_Min = -0.0015000000000000000312250225675825276994
Y_Min = -0.0030486282601243420466163858151276144781
Z_Min = -0.0000007442940088194194449747035681463903
X_Max = 0.0045972565202486836283268800684709276538
Y_Max = 0.0030486282601243420466163858151276144781
Z_Max = 0.0000007442940088194194449747035681463903


# --- Declare Settings Lists --- #
axesSettings = []
plotSettings = []


# --- Define Axes --- #
axesSettings1 = dict(name='XY',
                     shape=(2, 2),
                     loc=(0, 0),
                     rowspan=2,
                     colspan=2,
                     xlim=[X_Min, X_Max],
                     ylim=[Y_Min, Y_Max],
                     xlabel='$x$',
                     xunits=r'\textmu m',
                     xunits_value=1e-4,
                     xticks_out=True,
                     ylabel='$y$',
                     yunits=r'\textmu m',
                     yunits_value=1e-4,
                     yticks_out=True,
                     aspect='equal')

axesSettings2 = dict(name='XY_inset',
                     parent_axes='XY',
                     zoom=2,
                     loc=4,
                     xlim=[X_Min / 5, X_Max / 5],
                     ylim=[Y_Min / 5, Y_Max / 5],
                     visible_xticks=False,
                     visible_yticks=False,
                     loc1=1,
                     loc2=3,
                     ec="0.75")

axesSettings3 = dict(name='Ex2D_cbar',
                     position=[0.85, 0.7, 0.025, 0.25])

axesSettings4 = dict(name='Electron2D_cbar',
                     position=[0.85, 0.4, 0.025, 0.25])

axesSettings5 = dict(name='Proton2D_cbar',
                     position=[0.85, 0.1, 0.025, 0.25])

axesSettings6 = dict(name='XY_inset_inset',
                     parent_axes='XY_inset',
                     zoom=2,
                     loc=1,
                     xlim=[-1e-4, 1e-4],
                     ylim=[-1e-4, 1e-4],
                     visible_xticks=False,
                     visible_yticks=False,
                     loc1=2,
                     loc2=4,
                     ec="0.75")


# --- Define Plots --- #
plotSettings1 = dict(name='Ex2D',
                     ax='XY',
                     data_type='float',     # metadata
                     plot_type='rgba',
                     size=(1024, 1024),     # metadata
                     xMin=X_Min,            # metadata
                     xMax=X_Max,            # metadata
                     yMin=Y_Min,            # metadata
                     yMax=Y_Max,            # metadata
                     cmap='seismic',
                     clim=(-2.5e8, 2.5e8),
                     norm='linear',
                     show_cbar=True,
                     cax='Ex2D_cbar',
                     cbarlabel=r'$E_x$',
                     cbarunits=r'cgs')

plotSettings2 = dict(name='Electron2D',
                     ax='XY',
                     data_type='float',     # metadata
                     plot_type='rgba',
                     size=(1024, 1024),     # metadata
                     xMin=X_Min,            # metadata
                     xMax=X_Max,            # metadata
                     yMin=Y_Min,            # metadata
                     yMax=Y_Max,            # metadata
                     cmap='GreenBlack',
                     clim=(1e4, 1e7),
                     norm='logarithmic',
                     show_cbar=True,
                     cax='Electron2D_cbar',
                     cbarlabel=r'$N_e$',
                     cbarunits=r'cgs')

plotSettings3 = dict(name='Proton2D',
                     ax='XY',
                     data_type='float',     # metadata
                     plot_type='rgba',
                     size=(1024, 1024),     # metadata
                     xMin=X_Min,            # metadata
                     xMax=X_Max,            # metadata
                     yMin=Y_Min,            # metadata
                     yMax=Y_Max,            # metadata
                     cmap='RdPu',
                     clim=(1e3, 1e5),
                     norm='logarithmic',
                     show_cbar=True,
                     cax='Proton2D_cbar',
                     cbarlabel=r'$N_p$',
                     cbarunits=r'cgs')


axesSettings.append(axesSettings1)
axesSettings.append(axesSettings2)
axesSettings.append(axesSettings3)
axesSettings.append(axesSettings4)
axesSettings.append(axesSettings5)
axesSettings.append(axesSettings6)

plotSettings.append(plotSettings1)
plotSettings.append(plotSettings2)
plotSettings.append(plotSettings3)

plotSettings.append(plotSettings1.copy())
plotSettings.append(plotSettings2.copy())
plotSettings.append(plotSettings3.copy())
plotSettings.append(plotSettings1.copy())
plotSettings.append(plotSettings2.copy())
plotSettings.append(plotSettings3.copy())
plotSettings[3]['ax'] = 'XY_inset'
plotSettings[4]['ax'] = 'XY_inset'
plotSettings[5]['ax'] = 'XY_inset'
plotSettings[6]['ax'] = 'XY_inset_inset'
plotSettings[7]['ax'] = 'XY_inset_inset'
plotSettings[8]['ax'] = 'XY_inset_inset'

plot.Plot(axesSettings, plotSettings)
