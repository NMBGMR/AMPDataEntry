import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
import seaborn as sns
from mpl_toolkits.axes_grid1 import host_subplot
import numpy as np
import matplotlib.dates as mdates
import time

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

def plot_stuff(data_df, wl_df, precip_df):
    """"""

    # precip and usage time series
    time_series1 = data_df['Period']
    precip_series_list = data_df['Period'].tolist()
    print 'len', len(precip_series_list)
    print 'len', len(data_df['Maggie_Precip_mm'].tolist())
    precip_series = np.linspace(0, len(precip_series_list))

    #water level time series
    time_series2 = wl_df['new_date']

    # precip_time_series
    precip_time_series = precip_df['DATE']

    # fmt = mdates.DateFormatter('%Y/%m/%d')
    #
    # figure, ax = plt.subplots()
    #
    # plt.style.use('seaborn-notebook')
    # ax.set_title('precip as bar graphs')
    # ax.set_xlabel('Date')
    # ax.set_ylabel('Precip in mm')
    # precip_df[]
    # plt.show()

    # TODO - do a stacked plot for the bar plot.
    # # ====== First Plot Trujillo ======
    # host = host_subplot(111, axes_class=AA.Axes)
    # plt.subplots_adjust(right=0.75)
    #
    # plt.style.use('seaborn-notebook')
    # # sns.set_style('white')
    #
    # host.set_title('Withdrawals, Precipitation and Waterlevels in Trujillo Well Magdalena NM')
    #
    # par1 = host.twinx()
    # par2 = host.twinx()
    # # par3 = host.twinx()
    #
    # offset = 60
    # new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    # par2.axis['right'] = new_fixed_axis(loc='right', axes=par2, offset=(offset, 0))
    #
    # par1.axis['right'].toggle(all=True)
    # par2.axis['right'].toggle(all=True)
    #
    # host.set_xlabel('Date')
    # host.set_ylabel('Depth to Water (ft bgs)')
    # # we want the graph to show depth increasing DOWN the y-axis
    # host.set_ylim(120, 104)
    # par1.set_ylabel('Gallons x 100,000/month withdrawn')
    # # we want the gallons per month to show in scientific notation
    # # par1.ticklable_format(style='sci', axis='y', scilimits=(0, 0))
    #
    # par2.set_ylabel('Precipitation in mm')
    #
    # p1, = host.plot(pd.to_datetime(time_series2), wl_df['DepthToWaterBGS'], color='g', label='Trujillo Test Well')
    # p2, = par1.plot(pd.to_datetime(time_series1), data_df['trujillo_hundredthou'], color='b', label='Trujillo Well')
    # # todo convert datetime to float time since
    # # pd.apply(pd.to_datetime(precip_time_series))
    # def func(time_series):
    #     return time.mktime(time_series.timetuple())
    # xs = pd.to_datetime(precip_time_series).apply(func)
    #
    # args = par2.bar(xs, precip_df['PRCP'], color='r', label='Magdalena Met. Station')
    # print 'args', args
    #
    # host.legend(bbox_to_anchor=(0.5, -0.06), loc='upper center', ncol=4)
    #
    # host.axis['left'].label.set_color(p1.get_color())
    # par1.axis['right'].label.set_color(p2.get_color())
    # # par2.axis['right'].label.set_color(p4.get_color())
    #
    # # todo - figure out issue with bar plot and dates on monday.
    # plt.show()

    # ====== SECOND Plot Benjamin ======
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)

    plt.style.use('seaborn-notebook')
    # sns.set_style('white')

    host.set_title('Withdrawals, Precipitation and Waterlevels in Benjamin Well Magdalena NM')

    par1 = host.twinx()
    par2 = host.twinx()
    # par3 = host.twinx()

    offset = 60
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis['right'] = new_fixed_axis(loc='right', axes=par2, offset=(offset, 0))

    par1.axis['right'].toggle(all=True)
    par2.axis['right'].toggle(all=True)

    host.set_xlabel('Date')
    host.set_ylabel('Depth to Water (ft bgs)')
    # we want the graph to show depth increasing DOWN the y-axis
    host.set_ylim(120, 104)
    par1.set_ylabel('Gallons x 100,000/month withdrawn')
    # we want the gallons per month to show in scientific notation
    # par1.ticklable_format(style='sci', axis='y', scilimits=(0, 0))

    par2.set_ylabel('Precipitation in mm')

    p1, = host.plot(pd.to_datetime(time_series2), wl_df['DepthToWaterBGS'], color='g', label='Trujillo Test Well')
    p2, = par1.plot(pd.to_datetime(time_series1), data_df['benjamin_hundredthou'], '--', color='b',
                    label='Benjamin Well')
    p4, = par2.plot(pd.to_datetime(precip_time_series), precip_df['PRCP'], color='r', label='Magdalena Met. Station')

    host.legend(bbox_to_anchor=(0.5, -0.06), loc='upper center', ncol=4)

    host.axis['left'].label.set_color(p1.get_color())
    par1.axis['right'].label.set_color(p2.get_color())
    par2.axis['right'].label.set_color(p4.get_color())

    # todo - figure out issue with bar plot and dates on monday.
    plt.show()


def main(data_path, waterlevel_path, precip_path):
    """"""

    # read data
    data_df = pd.read_csv(data_path)
    wl_df = pd.read_csv(waterlevel_path)
    precip_df = pd.read_csv(precip_path)

    # create usage columns with gallons in 10,000 gallon units
    data_df['trujillo_hundredthou'] = data_df['trujillo_usage'] / 100000.0
    data_df['benjamin_hundredthou'] = data_df['benjamin_usage'] / 100000.0
    print 'data df \n', data_df

    # fix dates
    wl_df = fix_dates(wl_df, data_df)
    plot_stuff(data_df, wl_df, precip_df)


if __name__ == "__main__":

    data_path = 'Z:\data\datasets\magdalena_wells\magdalena_wells_17_18.csv'
    waterlevel_path = 'Z:\data\datasets\magdalena_wells\WaterLevelsContinuous_Pressure_mg_038_0717_1118_for_import.csv'
    precipitation_path = 'Z:\data\datasets\magdalena_wells\magdalena_kellyranch_weather.csv'

    main(data_path, waterlevel_path, precipitation_path)