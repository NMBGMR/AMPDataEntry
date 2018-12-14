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
    data_path = '~/Downloads/magdalena_wells_17_18.csv'
    waterlevel_path = '~/Downloads/WaterLevelsContinuous_Pressure_mg_038_0717_1118_for_import.csv'
    precipitation_path = '~/Downloads/magdalena_kellyranch_weather.csv'

    wd_df = pd.read_csv(data_path)
    wl_df = pd.read_csv(waterlevel_path)
    precip_df = pd.read_csv(precipitation_path)

    # create usage columns with gallons in 10,000 gallon units
    # wd_df['trujillo_hundredthou'] = wd_df['trujillo_usage'] / 100000.0
    # wd_df['benjamin_hundredthou'] = wd_df['benjamin_usage'] / 100000.0
    # print 'data df \n', wd_df

    # fix dates
    fix_dates(wl_df)

    return wd_df, wl_df, precip_df


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


def plot(wd_df, wl_df, precip_df):
    fig, (ax1, ax2) = plt.subplots(2)

    wl_xs, wl_ys = get_water_levels(wl_df)
    # plot water levels
    ax2.plot(wl_xs, wl_ys)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Depth to Water (ft bgs)')
    ax2.invert_yaxis()

    # plot withdraws
    wd_xs, wd_ys = get_withdrawals(wd_df, 'benjamin_usage')
    ax2_right = ax2.twinx()
    ax2_right.plot(wd_xs, wd_ys)
    ax2_right.set_ylabel('Gallons x 100,000/month withdrawn')

    # plot precip
    p_xs, p_ys = get_precip(precip_df)
    ax1.bar(p_xs, p_ys)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Precipitation (mm)')

    # # set x limits to the same values
    wl_xs = datetimes_to_floats(wl_xs)
    wd_xs = datetimes_to_floats(wd_xs)

    min_xs = min(min(wl_xs), min(wd_xs), min(p_xs))
    max_xs = max(max(wl_xs), max(wd_xs), max(p_xs))

    ax1.set_xlim(min_xs, max_xs)
    ax1.get_xaxis().set_visible(False)

    plt.show()


def main():
    plot(*get_data())


if __name__ == '__main__':
    main()

# ============= EOF =============================================
