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
# something is wrong with the import of geopandas
import geopandas
from shapely.geometry import Point
import matplotlib.pyplot as plt

# ============= local library imports ===========================

def parse_well_sites_df(sites_df):
    """"""

    # 2) For Sites, delete duplicates of USGS IDs

    sites_df = sites_df.drop_duplicates("SiteID")
    print(sites_df.shape, '\n sites df, duplictes removed\n')

    # 2a) For Sites, pull sites that are missing corresponding waterlevels...

    # pull values for sites that are completely blank.
    print('the columns\n', sites_df.iloc[:, 1:].columns)
    sites_df = sites_df[sites_df.iloc[:, 1:].notnull()]
    # there don't appear to be any that are completely blank
    print('completely null \n', sites_df.shape)

    # # TODO - pull only if the null values have the correct code
    # # Don't pull if D - Dry, C - Frozen, F - Flowing, I - Injection, K- Cascading water, O - Obstruction, W - Well destroyed, Z - Other
    acceptable_null_codes = ['D', 'C', 'F', 'I', 'K', 'O', 'W', 'Z']

    print('test', sites_df.WLStatus.isin(acceptable_null_codes).head())
    print('test2', sites_df.WLBelowLSD.notnull())

    # todo - us the acceptable null wls mask to get rid of the rest of the nulls that are unacceptable from the sites_df
    acceptable_null_wls_mask = sites_df.WLBelowLSD.isnull() & sites_df.WLStatus.isin(acceptable_null_codes)
    good_null_sites_df = sites_df[sites_df.WLBelowLSD.isnull() & sites_df.WLStatus.isin(acceptable_null_codes)]
    print('blank but has an acceptable code\n', good_null_sites_df.shape)

    # make sure the water levels are either intergers or floats. Other values are not acceptable i.e. "-. 4"
    sites_df = sites_df[pd.to_numeric(sites_df["WLBelowLSD"],
                                      errors='coerce').notnull()]
    print('sites and waterlevels with no corresponding waterlevel\n', sites_df.shape)

    return sites_df

def format_to_csv():
    waterlevel_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/NMBGR_20160908.xlsx"
    raw_data = pd.read_excel(waterlevel_path, sheet_name="gw.wls.subf")

    # output to a csv
    output_waterlevel_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/NMBGR_20160908.csv"
    raw_data.to_csv(output_waterlevel_path)

def geo_pandas_parse(reg_dataframe, nm_county_path=None, tx_county_path=None, co_county_path=None, az_county_path=None):
    """"""
    # from the dataframe, get the latitude and longitude and convert it into a geodataframe.
    reg_dataframe["Coordinates"] = list(zip(reg_dataframe.Longitude, reg_dataframe.Latitude))
    reg_dataframe['Coordinates'] = reg_dataframe['Coordinates'].apply(Point)

    geo_df = geopandas.GeoDataFrame(reg_dataframe, geometry='Coordinates')
    # print('geo df', geo_df)

    # set the geo dataframe crs to the nm crs
    geo_df.crs = {'init': 'espg 4269'}

    #
    print('geo dataframe head', geo_df.head())

    nm_countines = geopandas.read_file(nm_county_path)
    tx_counties = geopandas.read_file(tx_county_path)
    co_counties = geopandas.read_file(co_county_path)
    az_counties = geopandas.read_file(az_county_path)

    # tx_counties.crs = nm_countines.crs



    print('nm crs', nm_countines.crs)
    print('co crs', co_counties.crs)
    print('tx crs', tx_counties.crs)

    print(' NM counties df\n', nm_countines.head())
    print('TX counties df\n', tx_counties.head())
    print('CO counties df\n', co_counties.head())
    print('AZ border counties df\n', az_counties.head())

    figure, ax = plt.subplots(1)

    nm_countines.plot(ax=ax)
    co_counties.plot(ax=ax)
    tx_counties.plot(ax=ax)
    az_counties.plot(ax=ax)

    # ax = nm_countines.plot(edgecolor='black')

    geo_df.plot(ax=ax, color='red')

    plt.show()

def rename_cols(df):

    # get rid of the index column
    df = df.drop(labels=['Unnamed: 0'], axis=1)

    cols = df.columns.tolist()

    cols = [col.strip() for col in cols]

    cols = [col.replace(" ", "") for col in cols]

    cols = [col.split('C')[-1][3:] for col in cols]

    print('columns \n', cols)

    # based on cols, we hardcode new site names which are easier to reference and don't have all kinds of annoying space
    cols_new = ['SiteID', 'WellNumber', 'StationName', 'OtherID', 'CountyCode',
                'Latitude', 'Longitude', 'MethodLatLong',
                'LatLongAccuracy', 'LSAltitude', 'AltitudeDatum', 'AltitudeMethod',
                'AltitudeAccuracy', 'HoleDepth', 'WellDepth', 'WellConstructionDate', 'SiteUse',
                'WaterUse', 'AquiferCode', 'WLMeasurementDate', 'MeasurementTime',
                'WLTimeDatum', 'WLBelowLSD', 'WLStatus', 'AccuracyCode',
                'WLMethod', 'SourceAgency', 'WLApprovalStatus']

    df.columns = cols_new

    print('new columns for DF', df.columns)

    return df

def main(waterlevel_path, county_paths):
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
    pd.set_option('display.max_columns', None)
    # print('data \n', raw_data.iloc[:10, 23])

    # ==== Automated Parsing Steps ====

    # ======= WELL SITES ========

    # 1) Separate Sites and Water Levels into two separate dataframes

    sites_df = raw_data
    water_levels = raw_data

    # todo - keep developing parse_well_sites_df according to Kitty's instructions.
    parsed_sites = parse_well_sites_df(sites_df)

    # ***** Todo - At this stage, compare with SQL database to see which sites are new before checking geographic info.

    # 2b) For Sites, pull sites that have coordinates outside of New Mexico
    geo_pandas_parse(sites_df, nm_county_path=county_paths['nm'], tx_county_path=county_paths['tx'],
                     co_county_path=county_paths['co'], az_county_path=county_paths['az'])

    # 2c) For Sites, pull Sites with null water levels below MP (dry wells)
    # todo - ask kitty if the MP needs to come from the sql database?

    # ======= WATER LEVELS ========

    # 3) For Water Levels, pull out rows with no water level
    water_levels = raw_data[raw_data["WLBelowLSD"].notnull()]
    # print('waterlevel rows with no waterlevel', water_levels)


    # 4) Remove WL's for sites not in New Mexico or that have no coordinates [using 2b]

    # 5) Remove WL's measured below MP or that are Null

    # 6) Remove WL's that actually are blank and have no WL, that are dry, destroyed, obstructed or are
    #  flowing(artesian)

    # ===== Non Automatic Parsing [Interactive?] ====

    # to be continued...


if __name__ == "__main__":

    # # format to csv. Only do this once
    # format_to_csv()

    # waterlevel_path = "Z:\data\datasets\USGSWaterLevelData\USGS WL New Pull 2016\NMBGR_20160908.csv"
    waterlevel_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/NMBGR_20160908.csv"


    # paths to shapefiles to geographically parse sites
    nm_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/provision-878783/fe_2007_35_county.shp"
    tx_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/political-bnd_tx/txdot-counties/" \
                     "txdot_2015_county_detailed_tx.shp"
    co_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/" \
                     "Colorado_County_Boundaries/Colorado_County_Boundaries.shp"
    az_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/AZ_border_counties/AZ_border_counties.shp"
    county_paths = {'nm': nm_county_path, 'tx': tx_county_path, 'co': co_county_path, 'az': az_county_path}

    main(waterlevel_path, county_paths)