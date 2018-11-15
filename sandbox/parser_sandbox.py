# ===============================================================================
# Copyright 2018 gabe-parrish
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

# ============= standard library imports ========================
import os
import pandas as pd
import geopandas
from shapely.geometry import Point
import matplotlib.pyplot as plt

# ============= local library imports ===========================

def format_to_csv():
    waterlevel_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/NMBGR_20160908.xlsx"
    raw_data = pd.read_excel(waterlevel_path, sheet_name="gw.wls.subf")

    # output to a csv
    output_waterlevel_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/NMBGR_20160908.csv"
    raw_data.to_csv(output_waterlevel_path)

def geo_pandas_parse(reg_dataframe):
    """"""
    # from the dataframe, get the latitude and longitude and convert it into a geodataframe.
    reg_dataframe["Coordinates"] = list(zip(reg_dataframe.Longitude, reg_dataframe.Latitude))
    reg_dataframe['Coordinates'] = reg_dataframe['Coordinates'].apply(Point)

    geo_df = geopandas.GeoDataFrame(reg_dataframe, geometry='Coordinates')
    print 'geo df', geo_df
    #
    # print 'geo dataframe head', geo_df.head()
    #
    # nm_countines = geopandas.read_file("Z:\data\datasets\USGSWaterLevelData\USGS WL New Pull 2016\GIS Files\\fe_2007_35_county.shp")
    #
    # ax = nm_countines.plot(color='white', edgecolor='black')

    geo_df.plot(color='red')

    plt.show()

def rename_cols(df):

    # get rid of the index column
    df = df.drop(labels=['Unnamed: 0'], axis=1)

    cols = df.columns.tolist()

    cols = [col.strip() for col in cols]

    cols = [col.replace(" ", "") for col in cols]

    cols = [col.split('C')[-1][3:] for col in cols]

    print 'columns \n', cols

    # based on cols, we hardcode new site names which are easier to reference and don't have all kinds of annoying space
    cols_new = ['SiteID', 'WellNumber', 'StationName', 'OtherID', 'CountyCode',
                'Latitude', 'Longitude', 'MethodLatLong',
                'LatLongAccuracy', 'LSAltitude', 'AltitudeDatum', 'AltitudeMethod',
                'AltitudeAccuracy', 'HoleDepth', 'WellDepth', 'WellConstructionDate', 'SiteUse',
                'WaterUse', 'AquiferCode', 'WLMeasurementDate', 'MeasurementTime',
                'WLTimeDatum', 'WLBelowLSD', 'WLStatus', 'AccuracyCode',
                'WLMethod', 'SourceAgency', 'WLApprovalStatus']

    df.columns = cols_new

    print 'new columns for DF', df.columns

    return df

def main(waterlevel_path):
    """
    We're parsing the water level data as given to NMBGMR as was done by Kitty Pokorny.
    :return:
    """
    # first thing is to read in the file as a pandas dataframe, then we'll start parsing it.
    raw_data = pd.read_csv(waterlevel_path)

    # let's rename the columns so that they are easier to reference later on
    raw_data = rename_cols(raw_data)

    # todo vvvvv
    # 25   C276   Accuracy code <-&&&&&&&-> 23   C237   Water-level below LSD have mixed datatypes

    # # This is to make the full dataframe display
    # pd.set_option('display.max_columns', None)

    print('data \n', raw_data.iloc[:10, 23])

    # ==== Automated Parsing Steps ====

    # ======= WELL SITES ========

    # 1) Separate Sites and Water Levels two separate dataframes

    sites_df = raw_data
    water_levels = raw_data

    # 2) For Sites, delete duplicates of USGS IDs

    sites_df = sites_df.drop_duplicates("SiteID")
    print(sites_df, '\n sites df, duplictes removed\n')

    # 2a) For Sites, pull sites that are missing corresponding waterlevels...

    # TODO - pull only if the null values have the correct code
    # Don't pull if D - Dry, C - Frozen, F - Flowing, I - Injection, K- Cascading water, O - Obstruction, W - Well destroyed, Z - Other
    sites_df = sites_df[sites_df["WLBelowLSD"].notnull()]

    # make sure the water levels are either intergers or floats. Other values are not acceptable i.e. "-. 4"
    sites_df = sites_df[pd.to_numeric(sites_df["WLBelowLSD"],
                           errors='coerce').notnull()]
    print('sites and waterlevels with no corresponding waterlevel\n', sites_df)

    # ***** At this stage, compare with SQL database to see which sites are new before checking geographic info.

    # 2b) For Sites, pull sites that have coordinates outside of New Mexico
    # todo - geopandas example gallery 'creating a geodataframe from a regular dataframe with coordinates'
    geo_pandas_parse(sites_df)

    # 2c) For Sites, pull Sites with null water levels below MP (dry wells)
    # todo - ask kitty if the MP needs to come from the sql database?

    # ======= WATER LEVELS ========


    # 3) For Water Levels, pull out rows with no water level
    water_levels = raw_data[raw_data["23   C237   Water-level below LSD                             "].notnull()]
    print('waterlevel rows with no waterlevel', water_levels)


    # 4) Remove WL's for sites not in New Mexico or that have no coordinates [using 2b]

    # 5) Remove WL's measured below MP or that are Null

    # 6) Remove WL's that actually are blank and have no WL, that are dry, destroyed, obstructed or are
    #  flowing(artesian)

    # ===== Non Automatic Parsing [Interactive?] ====

    # to be continued...


if __name__ == "__main__":

    # # format to csv. Only do this once
    # format_to_csv()

    waterlevel_path = "Z:\data\datasets\USGSWaterLevelData\USGS WL New Pull 2016\NMBGR_20160908.csv"

    main(waterlevel_path)

    # 2a scratch
    # # make a dataframe of sites and waterlevels from the raw_data, then purge the sites missing waterlevel data. sites that are left you remove from sites_df
    #
    # sites_and_waterlevels = raw_data[["1   C001   Site ID (station number)                          ",
    #                                   "23   C237   Water-level below LSD                             "]]
    # print('pre drop\n', sites_and_waterlevels)
    # sites_and_waterlevels = sites_and_waterlevels.dropna()
    # print('post drop\n', sites_and_waterlevels)
    # sites_and_waterlevels = sites_and_waterlevels.drop_duplicates("1   C001   Site ID (station number)                          ")
    # print('sites and waterlevels with no corresponding waterlevel\n', sites_and_waterlevels) # todo - i get a number different from kitty p. here: 28453. Kitty had 28625

    # sites_cols = ["1   C001   Site ID (station number)                          ",
    #               "3   C900   Station name                                      ",
    #               "4   C190   Other identifier                                  ",
    #               "5   C008   County code                                       ",
    #               "6   C909   Latitude NAD83 in decimal degrees                 ",
    #               "7   C910   Longitude NAD83 in decimal degrees                ",
    #               "8   C035   Method Lat/Long Determined                        ",
    #               "9   C011   Lat/Long accuracy code                            ",
    #               "10   C016   Altitude of land surface                          ",
    #               "11   C022   Altitude Datum                                    ",
    #               "12   C017   Method altitude determined                        ",
    #               "13   C018   Altitude accuracy                                 ",
    #               "14   C027   Hole depth                                        ",
    #               "15   C028   Well depth                                        ",
    #               "16   C021   Date well constructed                             ",
    #               "17   C023   Primary use of site                               ",
    #               "18   C024   Primary use of water                              ",
    #               "19   C714   Aquifer code                                      "]
    #                #                  "23   C237   Water-level below LSD                             "