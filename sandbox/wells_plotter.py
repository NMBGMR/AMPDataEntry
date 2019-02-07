# ===============================================================================
# Copyright 2018 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import time

import matplotlib.pyplot as plt
import pandas as pd
# import datetime.datetime as dt

def date_lucid(df):
    """"""
    dates = pd.to_datetime(df['DateMeasured'])
    df['new_date'] = dates

def fix_dates(df):
    """"""
    dates = pd.to_datetime(df['DateMeasured'])

    new_dates = []
    for i, row in dates.iteritems():
        if i % 2 == 0:
            row = row.replace(hour=0)
            new_dates.append(row)
        else:
            row = row.replace(hour=12)
            new_dates.append(row)

    new_dates = pd.Series(new_dates)
    df['new_date'] = new_dates


def get_data():
    data_path = 'Z:\data\datasets\magdalena_wells\magdalena_wells_17_18.csv'
    trujillo_waterlevel_path = 'Z:\data\datasets\magdalena_wells\TrujilloWaterLevelsContinuous_Pressure_mg_038_0717_1118_for_import.csv'
    danielson_wl_path = 'Z:\data\datasets\magdalena_wells\DanielsonWaterLevelsContinuous_Pressure_for_import.csv'
    precipitation_path = 'Z:\data\datasets\magdalena_wells\magdalena_kellyranch_weather.csv'

    wd_df = pd.read_csv(data_path)
    trujillo_wl_df = pd.read_csv(trujillo_waterlevel_path)
    danielson_wl_df = pd.read_csv(danielson_wl_path)
    precip_df = pd.read_csv(precipitation_path)

    # print 'danielson_wl_df', danielson_wl_df

    # fix dates
    date_lucid(trujillo_wl_df)
    date_lucid(danielson_wl_df)

    # get rid of Data for Danielson well before July 2017
    danielson_wl_df = danielson_wl_df[(danielson_wl_df['new_date'].dt.year >= 2017) & (danielson_wl_df['new_date'].dt.month >= 07)]

    # print 'trujillos\n', trujillo_wl_df['new_date']

    # # fix dates
    # fix_dates(trujillo_wl_df)


    return wd_df, danielson_wl_df, trujillo_wl_df, precip_df


def get_water_levels(wl_df):
    ys = wl_df['DepthToWaterBGS']
    xs = pd.to_datetime(wl_df['new_date'])
    return xs[::2], ys[::2]


def get_withdrawals(df, tag, scale=1e6):
    ys = df[tag] / scale
    xs = pd.to_datetime(df['Period'])
    return xs, ys


def get_precip(df):
    xs = pd.to_datetime(df['DATE'])
    ys = df['PRCP']
    xs = datetimes_to_floats(xs)
    return xs, ys


def datetimes_to_floats(ds):
    return [time.mktime(di.timetuple()) for di in ds]


def plot(wd_df, danielson_wl_df, trujillo_wl_df, precip_df):

    # ===== Benjamin =====
    fig, (ax1, ax2) = plt.subplots(2)
    fig.subplots_adjust(hspace=0)

    fig.suptitle('Withdrawals, Precipitation and Waterlevels in Benjamin Well Magdalena, NM', size='20')
    # plt.style.use('seaborn-notebook')
    plt.style.use('seaborn-pastel')

    wl_xs, wl_ys = get_water_levels(danielson_wl_df)
    # plot water levels
    ax2.plot(wl_xs, wl_ys, color='b', linewidth=2.0, label='Danielson Well')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Depth to Water (ft bgs)', color='b')
    ax2.invert_yaxis()

    # plot withdrawals
    wd_xs, wd_ys = get_withdrawals(wd_df, 'benjamin_usage')
    ax2_right = ax2.twinx()
    ax2_right.plot(wd_xs, wd_ys, color='g', linewidth=3.0, label='Benjamin Well')
    ax2_right.set_ylabel('Gallons x 100,000/month withdrawn', color='g')

    # plot precip
    p_xs, p_ys = get_precip(precip_df)
    ax1.bar(p_xs, p_ys, color='k', label='Magdalena Met. Station')
    # ax1.yaxis.tick_right()
    for i, label in enumerate(ax1.get_yticklabels()):
        if i == 0:
            label.set_visible(False)

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Precipitation (mm)', color='r')

    # # set x limits to the same values
    wl_xs = datetimes_to_floats(wl_xs)
    wd_xs = datetimes_to_floats(wd_xs)

    min_xs = min(min(wl_xs), min(wd_xs), min(p_xs))
    max_xs = max(max(wl_xs), max(wd_xs), max(p_xs))

    ax1.set_xlim(min_xs, max_xs)
    ax1.get_xaxis().set_visible(False)

    ax1.legend(loc='upper right', prop={'size': 10})
    ax2.legend(loc='upper center', prop={'size': 10})
    ax2_right.legend(loc='lower center', prop={'size': 10})

    plt.show()

    # ===== Trujillo =====
    fig, (ax1, ax2) = plt.subplots(2)
    fig.subplots_adjust(hspace=0)

    fig.suptitle('Withdrawals, Precipitation and Waterlevels in Trujillo Well Magdalena, NM', size=20)
    # plt.style.use('seaborn-notebook')

    wl_xs, wl_ys = get_water_levels(trujillo_wl_df)
    # plot water levels
    tw_test = ax2.plot(wl_xs, wl_ys, color='b', linewidth=2.0, label='Trujillo Test Well')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Depth to Water (ft bgs)', color='b')
    ax2.invert_yaxis()

    # plot withdrawals
    wd_xs, wd_ys = get_withdrawals(wd_df, 'trujillo_usage')
    ax2_right = ax2.twinx()
    tw = ax2_right.plot(wd_xs, wd_ys, color='g', linewidth=3.0, label='Trujillo Well')
    ax2_right.set_ylabel('Gallons x 100,000/month withdrawn', color='g')

    # plot precip
    p_xs, p_ys = get_precip(precip_df)
    mag_met = ax1.bar(p_xs, p_ys, color='black', label='Magdalena Met. Station')
    # ax1.yaxis.tick_right()
    for i, label in enumerate(ax1.get_yticklabels()):
        if i == 0:
            label.set_visible(False)

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Precipitation (mm)', color='r')

    # # set x limits to the same values
    wl_xs = datetimes_to_floats(wl_xs)
    wd_xs = datetimes_to_floats(wd_xs)

    min_xs = min(min(wl_xs), min(wd_xs), min(p_xs))
    max_xs = max(max(wl_xs), max(wd_xs), max(p_xs))

    ax1.set_xlim(min_xs, max_xs)
    ax1.get_xaxis().set_visible(False)

    ax1.legend(loc='upper right', prop={'size':10})
    ax2.legend(loc='lower center', prop={'size':10})
    ax2_right.legend(loc='upper center', prop={'size':10})
    # fig.legend((tw_test, tw, mag_met), ('Magdalena Met. Station', 'Trujillo Test Well', 'Trujillo Well'), 'upper right')
    # plt.tight_layout()
    plt.show()


def main():
    # wd_df, trujillo_wl_df, danielson_wl_df, precip_df = get_data()

    plot(*get_data())


if __name__ == '__main__':
    main()

# ============= EOF =============================================
