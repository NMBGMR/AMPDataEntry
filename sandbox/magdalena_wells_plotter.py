import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
from mpl_toolkits.axes_grid1 import host_subplot

def fix_dates(wl_df, data_df):
    """"""
    dates = pd.to_datetime(wl_df['DateMeasured'])

    new_dates = []
    for i, row in dates.iteritems():
        if i % 2 == 0:
            row = row.replace(hour=0)
            new_dates.append(row)
        else:
            row = row.replace(hour=12)
            new_dates.append(row)

    new_dates = pd.Series(new_dates)
    wl_df['new_date'] = new_dates
    # print 'wl df \n', wl_df['new_date']

    # dates2 = pd.to_datetime()

    return wl_df

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def plot_stuff(data_df, wl_df):
    """"""

    # precip and usage time series
    time_series1 = data_df['Period']

    #water level time series
    time_series2 = wl_df['new_date']

    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()

    offset = 60
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis['right'] = new_fixed_axis(loc='right', axes=par2, offset=(offset, 0))

    par1.axis['right'].toggle(all=True)
    par2.axis['right'].toggle(all=True)

    host.set_xlabel('time')
    host.set_ylabel('Depth to Water (ft bgs)')
    par1.set_ylabel('gallons per month withdrawn')
    par2.set_ylabel('Precipitation in MM')

    p1, = host.plot(pd.to_datetime(time_series2), wl_df['DepthToWaterBGS'], color='g')
    p2, = par1.plot(pd.to_datetime(time_series1), data_df['trujillo_usage'], color='b')
    p3, = par1.plot(pd.to_datetime(time_series1), data_df['benjamin_usage'], color='b')
    p4, = par2.plot(pd.to_datetime(time_series1), data_df['Maggie_Precip_mm'], color='r')

    # todo - figure out issue with bar plot and dates on monday.
    plt.show()

    # # plt.bar(pd.to_datetime(time_series1), data_df['Maggie_Precip_mm'])
    # # plt.show(pd.to_datetime(time_series1), data_df[' Maggie_Precip_mm'], color='r')
    #
    # figure1, axis1 = plt.subplots()
    # axis1.plot(pd.to_datetime(time_series1), data_df['trujillo_usage'], color='b')
    # axis1.plot(pd.to_datetime(time_series1), data_df['benjamin_usage'], color='b')
    # axis1.set_xlabel('date')
    # axis1.set_ylabel('water usage in gallons', color='b')
    #
    #
    # axis2 = axis1.twinx()
    # # axis2.bar(pd.to_datetime(time_series1), data_df[' Maggie_Precip_mm'], color='r')
    # # axis2.xaxis_date()
    # axis2.plot(pd.to_datetime(time_series1), data_df['Maggie_Precip_mm'], color='r')
    # axis2.set_ylabel('precip', color='r')
    # plt.show()





def main(data_path, waterlevel_path):
    """"""

    # read data
    data_df = pd.read_csv(data_path)
    wl_df = pd.read_csv(waterlevel_path)

    print 'data df \n', data_df

    # fix dates
    wl_df= fix_dates(wl_df, data_df)

    plot_stuff(data_df, wl_df)


if __name__ == "__main__":

    data_path = 'Z:\data\datasets\magdalena_wells\magdalena_wells_17_18.csv'

    waterlevel_path = 'Z:\data\datasets\magdalena_wells\WaterLevelsContinuous_Pressure_mg_038_0717_1118_for_import.csv'

    main(data_path, waterlevel_path)