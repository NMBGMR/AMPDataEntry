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
import numpy as np

# ============= local library imports ===========================

def parse_well_sites_df(sites_df, filtered_data_path):
    """

    :param sites_df:
    :param filtered_data_path:
    :return:
    """

    # 2) For Sites, delete duplicates of USGS IDs

    print('original shape', sites_df.shape)

    sites_df = sites_df.drop_duplicates("SiteID")
    # print('\n sites df, duplictes removed\n', sites_df.shape)

    # 2a) For Sites, pull sites that are missing corresponding waterlevels...

    # pull values for sites that are completely blank.
    # print('the columns\n', sites_df.iloc[:, 19:].columns)
    blank_sites_mask = sites_df.iloc[:, 19:].notnull()

    blank_sites_mask = sites_df.iloc[:, 19].isnull() & sites_df.iloc[:, 20].isnull() & sites_df.iloc[:, 21].isnull()\
                       & sites_df.iloc[:, 22].isnull() & sites_df.iloc[:, 23].isnull() \
                       & sites_df.iloc[:, 24].isnull() & sites_df.iloc[:, 25].isnull() \
                       & sites_df.iloc[:, 26].isnull() & sites_df.iloc[:, 27].isnull()

    null_sites = sites_df[blank_sites_mask]
    # output completely blank wl sites to a file.
    null_sites.to_csv(os.path.join(filtered_data_path, 'completely_null_wls.csv'))
    # these are the sites that are completely blank
    # print('completely null \n', null_sites.shape)

    # # Don't pull values if WLStatus is D - Dry, C - Frozen, F - Flowing, I - Injection, K- Cascading water,
    #  O - Obstruction, W - Well destroyed, Z - Other
    acceptable_null_codes = ['D', 'C', 'F', 'I', 'K', 'O', 'W', 'Z']

    # how many sites have a null wl but have an acceptable code?
    acceptable_null_wls_mask = sites_df.WLBelowLSD.isnull() & sites_df.WLStatus.isin(acceptable_null_codes)
    good_null_sites_df = sites_df[sites_df.WLBelowLSD.isnull() & sites_df.WLStatus.isin(acceptable_null_codes)]
    # print('blank but has an acceptable code\n', good_null_sites_df.shape)

    # how many sites are null without a good code?
    unacceptable_null_wls_mask = sites_df.WLBelowLSD.isnull() & ~sites_df.WLStatus.isin(acceptable_null_codes)
    unacceptable_null_sites = sites_df[unacceptable_null_wls_mask]

    #output the unacceptable wls to a file
    unacceptable_null_sites.to_csv(os.path.join(filtered_data_path, 'null_values_w_bad_code.csv'))
    # print('blank and unacceptable code\n', sites_df[unacceptable_null_wls_mask].shape)

    # filter the blank sites and the un-acceptable nulls (inverse of acceptable nulls mask from the sites_df)

    # select the entries that are not blank and are acceptable nulls.
    sites_df = sites_df[~blank_sites_mask & ~unacceptable_null_wls_mask]

    # todo - are the values you're throwing out looking good?
    sites_df.to_csv(os.path.join(filtered_data_path, 'sites_df_post_filtering.csv'))
    # print('post blank and null filtering sites df shape', sites_df.shape)

    # # make sure the water levels are either intergers or floats. Other values are not acceptable i.e. "-. 4"
    # sites_df = sites_df[pd.to_numeric(sites_df["WLBelowLSD"],
    #                                   errors='coerce').notnull()]
    # print('sites and waterlevels with no corresponding waterlevel\n', sites_df.shape)

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

    nm_counties = geopandas.read_file(nm_county_path)
    tx_counties = geopandas.read_file(tx_county_path)
    co_counties = geopandas.read_file(co_county_path)
    az_counties = geopandas.read_file(az_county_path)

    # todo - join all the counties together in the same dataframe.

    # tx_counties.crs = nm_counties.crs

    # print('nm crs', nm_counties.crs)
    # print('co crs', co_counties.crs)
    # print('tx crs', tx_counties.crs)
    #
    print(' NM counties df\n', nm_counties.head())
    # print('TX counties df\n', tx_counties.head())
    # print('CO counties df\n', co_counties.head())
    # print('AZ border counties df\n', az_counties.head())



    # i want to write the county name that the point belongs to in the dataframe

    # made-up relationships for county codes to NM counties
    # 'McKinley: 377', 'Socorro: 243', 'Colfax: 023', 'Cibola: 141'
    # todo - expand this for AZ border counties, CO counties, and TX counties
    county_codes = {'McKinley': 31, 'Socorro': 53, 'Colfax': 7, 'Cibola': 6, 'Catron': 3,
                    'Torrance': 57,
                    'Lea': 25, 'Grant': 17, 'San Miguel': 47, 'Otero': 35, 'Santa Fe': 49, 'De Baca': 11,
                    'Luna': 29, 'Chaves': 5, 'Curry': 9, 'Hidalgo': 23, 'Valencia': 61, 'Union': 59,
                    'Bernalillo': 1, 'Lincoln': 27, 'Sierra': 51, 'Sandoval': 43, 'San Juan': 45,
                    'Guadalupe': 19, 'Quay': 37, 'Rio Arriba': 39, 'Taos': 55, 'Mora': 33, 'Roosevelt': 41,
                    'Eddy': 15, 'Harding': 21, 'Los Alamos': 28, 'Dona Ana': 13}

    # counties = []
    print('county codes', geo_df.CountyCode)
    # make a dictionary of how each county matches its coordinates in the site dataframe
    county_match_mask_dict = {}
    for index, county in enumerate(nm_counties.NAME.tolist()):
        print(county)
        poly = nm_counties.loc[index, 'geometry']
        # county_match_mask = geo_df.CountyCode == county_codes[county]
        # county_match_mask = geo_df.Coordinates.within(poly)
        county_match_mask = (geo_df.CountyCode == county_codes[county]) & (geo_df.Coordinates.within(poly))
        county_match_mask_dict[county] = county_match_mask
        # geo_df = geo_df[county_match_mask]

    # # testing for Catron County
    # catron_match = geo_df.CountyCode == 3
    # print('inside catron\n', nm_counties.loc[4, 'NAME'])
    # inside_catron = geo_df.Coordinates.within(nm_counties.loc[4, 'geometry'])
    # print('these should be inside Catron\n', catron_match)
    # catron_filter = (geo_df.CountyCode == 3) & (geo_df.Coordinates.within(nm_counties.loc[4, 'geometry']))

    # # print(counties)
    #
    # # join the bools TODO - figure out the actuall county codes so we can test whether or not this works...
    # bool_saver = np.zeros(geo_df.Coordinates.shape, dtype=bool)
    # for k, v in county_match_mask_dict.items():
    #     bool_saver | v
    #
    # # bool_saver
    #
    # print('bool save', bool_saver)
    #
    # # print( 'what this is?',pd.DataFrame(bool_saver))
    # # geo_df = geo_df[bool_saver]
    # geo_df = geo_df[pd.DataFrame(bool_saver)]


    # for k, v in county_match_mask_dict.items():
    #     # iteratively filter the geo dataframe for matching counties
    #     geo_df = geo_df[v]

    # ==== PLOTTING ====
    figure, ax = plt.subplots(1)

    nm_counties.plot(ax=ax)
    co_counties.plot(ax=ax)
    tx_counties.plot(ax=ax)
    az_counties.plot(ax=ax)

    # ax = nm_counties.plot(edgecolor='black')
    # # geo_df.plot(ax=ax, color='red')
    masked_dataframes = []
    for index, county in enumerate(nm_counties.NAME.tolist()):
        # print(' this is the county mask\n', county_match_mask_dict[county])
        mask = county_match_mask_dict[county]
        masked_df = geo_df[mask]
        # masked_df.plot(ax=ax)
        masked_dataframes.append(masked_df)
        # geo_df[mask].plot(ax=ax)

    print('masked data frames', masked_dataframes)
    for i in masked_dataframes:
        i.plot(ax=ax, color='red')

    plt.show()


    # catron_df = geo_df[catron_match]
    # catron_df.plot(ax=ax, color='red')
    #
    # plt.show()
    #
    # # ================= PLOT 2 =================
    #
    # figure1, ax1 = plt.subplots(1)
    #
    # nm_counties.plot(ax=ax1)
    # co_counties.plot(ax=ax1)
    # tx_counties.plot(ax=ax1)
    # az_counties.plot(ax=ax1)
    #
    # inside_catron_df = geo_df[inside_catron]
    #
    # inside_catron_df.plot(ax=ax1, color='red')
    #
    # plt.show()
    #
    # # ================= PLOT 3 =================
    #
    # figure2, ax2 = plt.subplots(1)
    #
    # nm_counties.plot(ax=ax2)
    # co_counties.plot(ax=ax2)
    # tx_counties.plot(ax=ax2)
    # az_counties.plot(ax=ax2)
    #
    # filter_catron_df = geo_df[catron_filter]
    #
    # filter_catron_df.plot(ax=ax2, color='red')
    #
    # plt.show()



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

def main(waterlevel_path, county_paths, filtered_data_path):
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
    parsed_sites = parse_well_sites_df(sites_df, filtered_data_path)

    # ***** Todo - At this stage, compare with SQL database to see which sites are new before checking geographic info.

    # 2b) For Sites, pull sites that have coordinates outside of New Mexico
    geo_pandas_parse(parsed_sites, nm_county_path=county_paths['nm'], tx_county_path=county_paths['tx'],
                     co_county_path=county_paths['co'], az_county_path=county_paths['az'])

    # 2c) For Sites, pull Sites with null water levels below MP (dry wells)
    # todo - ask kitty if the MP needs to come from the sql database?

    # # ======= WATER LEVELS ========
    #
    # # 3) For Water Levels, pull out rows with no water level
    # water_levels = raw_data[raw_data["WLBelowLSD"].notnull()]
    # # print('waterlevel rows with no waterlevel', water_levels)
    #
    #
    # # 4) Remove WL's for sites not in New Mexico or that have no coordinates [using 2b]
    #
    # # 5) Remove WL's measured below MP or that are Null
    #
    # # 6) Remove WL's that actually are blank and have no WL, that are dry, destroyed, obstructed or are
    # #  flowing(artesian)
    #
    # # ===== Non Automatic Parsing [Interactive?] ====
    #
    # # to be continued...


if __name__ == "__main__":

    # # format to csv. Only do this once
    # format_to_csv()

    # waterlevel_path = "Z:\data\datasets\USGSWaterLevelData\USGS WL New Pull 2016\NMBGR_20160908.csv"
    waterlevel_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/NMBGR_20160908.csv"

    # filtered data path - for outputting rejected data
    filtered_data_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/data_taken_out"


    # paths to shapefiles to geographically parse sites
    nm_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/provision-878783/fe_2007_35_county.shp"
    tx_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/political-bnd_tx/txdot-counties/txdot_2015_county_detailed_tx.shp"
    co_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/Colorado_County_Boundaries/Colorado_County_Boundaries.shp"
    az_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/AZ_border_counties/AZ_border_counties.shp"
    county_paths = {'nm': nm_county_path, 'tx': tx_county_path, 'co': co_county_path, 'az': az_county_path}

    main(waterlevel_path, county_paths, filtered_data_path)