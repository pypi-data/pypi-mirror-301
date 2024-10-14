from pathlib import Path
from AeroViz import plot, DataBase, DataClassifier


def use_scatter():
    # example of using plot.scatter
    df = DataBase(load_data=True)

    df = df[['Vis_LPV', 'PM2.5', 'RH', 'VC', 'Extinction', 'Scattering']].dropna()
    # plot.scatter(df, x='PM2.5', y='Extinction', c='VC', s='RH', cmap='YlGnBu', diagonal=True)
    plot.scatter(df, x='Scattering', y='Extinction', color='r', regression=True, regression_line_color='darkred',
                 diagonal=True)


def use_regression():
    # example of using plot.linear_regression
    df = DataBase(load_data=True)

    plot.linear_regression(df, x='PM2.5', y='Extinction')
    plot.linear_regression(df, x='PM2.5', y=['Extinction', 'Scattering', 'Absorption'], xlim=[0, None], ylim=[0, None])
    # plot.multiple_linear_regression(df, x=['AS', 'AN', 'OM', 'EC', 'SS', 'Soil'], y=['Extinction'])
    # plot.multiple_linear_regression(df, x=['NO', 'NO2', 'CO', 'PM1'], y=['PM25'])


def use_pie():
    pass


def use_bar():
    pass


def use_CBPF_windrose():
    # example of using plot.meteorology
    df = DataBase(load_data=True)

    # plot.meteorology.wind_rose(df, 'WS', 'WD', typ='bar')
    # plot.meteorology.wind_rose(df, 'WS', 'WD', 'PM25', typ='scatter')

    # plot.meteorology.CBPF(df, 'WS', 'WD', 'PM25')
    # plot.meteorology.CBPF(df, 'WS', 'WD', 'PM25', percentile=[0, 25])
    # plot.meteorology.CBPF(df, 'WS', 'WD', 'PM25', percentile=[25, 50])
    # plot.meteorology.CBPF(df, 'WS', 'WD', 'PM25', percentile=[50, 75])
    plot.meteorology.CBPF(df, 'WS', 'WD', 'PM2.5', percentile=[75, 100], resolution=50)


def use_SMPS():
    # example of using plot.distribution
    PNSD = DataBase(load_PSD=True)

    plot.distribution.heatmap(PNSD, unit='Number')
    plot.distribution.heatmap_tms(PNSD, unit='Number', freq='60d')

    # Classify the data
    # PNSD_state_class, _ = DataClassifier(df=PNSD, by='State', statistic='Table')
    # plot.distribution.plot_dist(PNSD_state_class, _, unit='Number', additional='error')

    # PNSE_ext_class, _ = DataClassifier(df=PNSD, by='Extinction', statistic='Table', qcut=20)
    # plot.distribution.three_dimension(PNSE_ext_class, unit='Number')

    # plot.distribution.curve_fitting(np.array(PNSE_ext_class.columns, dtype=float), PNSE_ext_class.iloc[0, :], mode=3, unit='Number')


def use_linear_regression_and_scatter_to_verify():
    # example of using plot.linear_regression and plot.scatter
    df = DataBase(load_data=True)

    plot.linear_regression(df, x='Extinction', y=['Bext_internal', 'Bext_external'], xlim=[0, 300], ylim=[0, 600])
    plot.linear_regression(df, x='Scattering', y=['Bsca_internal', 'Bsca_external'], xlim=[0, 300], ylim=[0, 600])
    plot.linear_regression(df, x='Absorption', y=['Babs_internal', 'Babs_external'], xlim=[0, 100], ylim=[0, 200])

    plot.scatter(df, x='Extinction', y='Bext_Fixed_PNSD', xlim=[0, 600], ylim=[0, 600], title='Fixed PNSD',
                 regression=True, diagonal=True)
    plot.scatter(df, x='Extinction', y='Bext_Fixed_RI', xlim=[0, 600], ylim=[0, 600], title='Fixed RI',
                 regression=True, diagonal=True)


def use_extinction_by_particle_gas():
    # example of using plot.bar and plot.pie
    df = DataBase(load_data=True)

    ser_grp_sta, ser_grp_sta_std = DataClassifier(df, by='State', df_support=df)
    ext_particle_gas = ser_grp_sta.loc[:, ['Scattering', 'Absorption', 'ScatteringByGas', 'AbsorptionByGas']]

    # plot.bar(data_set=ext_particle_gas, data_std=None,
    #          labels=[rf'$b_{{sp}}$', rf'$b_{{ap}}$', rf'$b_{{sg}}$', rf'$b_{{ag}}$'],
    #          unit='Extinction',
    #          style="stacked",
    #          colors=plot.Color.paired)

    plot.pie(data_set=ext_particle_gas,
             labels=[rf'$b_{{sp}}$', rf'$b_{{ap}}$', rf'$b_{{sg}}$', rf'$b_{{ag}}$'],
             unit='Extinction',
             style='donut',
             colors=plot.Color.paired,
             title=['', '', '', ''])


def use_timeseries():
    # example of using plot.timeseries
    df = DataBase(load_data=True)

    # plot.timeseries(df['2021-02-01':'2021-03-31'],
    #                 y=['Extinction', 'Scattering'], color=None, style=['line', 'line'],
    #                 ylim=[0, None], ylim2=[0, None], rolling=50,
    #                 inset_kws2=dict(bbox_to_anchor=(1.12, 0, 1.2, 1)))

    plot.timeseries(df['2021-02-01':'2021-02-11'],
                    y='WS', color='WD', style='scatter',
                    scatter_kws=dict(cmap='hsv'), cbar_kws=dict(ticks=[0, 90, 180, 270, 360]),
                    ylim=[0, None])

    # plot.timeseries_template(df.loc['2021-02-01':'2021-03-31'])


def use_diurnal_pattern():
    df = DataBase(load_data=True)
    plot.diurnal_pattern(df, 'PM2.5')


def use_hysplit():
    plot.hysplit(Path("/AeroViz/data/240228_00.txt"))

if __name__ == '__main__':
    # use_SMPS()
    # use_scatter()
    # use_regression()
    # use_CBPF_windrose()
    # use_extinction_by_particle_gas()
    # use_timeseries()
    # use_diurnal_pattern()
    use_hysplit()
