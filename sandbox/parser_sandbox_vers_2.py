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

def rename_cols(df):

    # get rid of the index column
    # df = df.drop(labels=['Unnamed: 0'], axis=1)

    cols = df.columns.tolist()

    cols = [col.strip() for col in cols]

    cols = [col.replace(" ", "") for col in cols]

    cols = [col.split('C')[-1][3:] for col in cols]

    print('columns \n', cols)

    # # based on cols, we hardcode new site names which are easier to reference and don't have all kinds of annoying space
    cols_new = ['SiteID', 'OtherID', 'StationName', 'CountyCode',
                'Latitude', 'Longitude', 'MethodLatLong',
                'LatLongAccuracy', 'LSAltitude', 'AltitudeDatum', 'AltitudeMethod',
                'AltitudeAccuracy', 'HoleDepth', 'WellDepth', 'WellConstructionDate', 'SiteUse',
                'LEVReadyForWebFlag']
    # # testing
    # cols_old = ['SiteID(stationnumber)', 'Otheridentifier', 'Stationname', 'tycode', 'LatitudeNAD83indecimaldegrees',
    #  'LongitudeNAD83indecimaldegrees', 'MethodLat/LongDetermined', 'Lat/Longaccuracycode',
    # 'Altitudeoflandsurface', 'AltitudeDatum', 'Methodaltitudedetermined', 'Altitudeaccuracy',
    #  'Holedepth', 'Welldepth', 'Datewellconstructed', 'Primaryuseofsite', 'LEVrecordreadyforwebflag']
    # print(len(cols_new ), len(cols_old))

    df.columns = cols_new
    print('new columns for DF', df.columns)
    return df

def geo_pandas_parse(reg_dataframe, filter_path, nm_county_path=None, tx_county_path=None, co_county_path=None, az_county_path=None):
    """"""

    # === from the dataframe, get the latitude and longitude and convert it into a geodataframe ===
    reg_dataframe["Coordinates"] = list(zip(reg_dataframe.Longitude, reg_dataframe.Latitude))
    reg_dataframe['Coordinates'] = reg_dataframe['Coordinates'].apply(Point)
    geo_df = geopandas.GeoDataFrame(reg_dataframe, geometry='Coordinates')

    # set the geo dataframe crs to the nm crs
    geo_df.crs = {'init': 'espg 4269'}

    print('geo dataframe head', geo_df.head())

    # read in the counties shapefiles
    nm_counties = geopandas.read_file(nm_county_path)
    tx_counties = geopandas.read_file(tx_county_path)
    co_counties = geopandas.read_file(co_county_path)
    az_counties = geopandas.read_file(az_county_path)

    # todo - expand this for AZ border counties, CO counties, and TX counties
    # the codes that correspond to each county in the spreadsheet
    county_codes = {'McKinley': 31, 'Socorro': 53, 'Colfax': 7, 'Cibola': 6, 'Catron': 3,
                    'Torrance': 57,
                    'Lea': 25, 'Grant': 17, 'San Miguel': 47, 'Otero': 35, 'Santa Fe': 49, 'De Baca': 11,
                    'Luna': 29, 'Chaves': 5, 'Curry': 9, 'Hidalgo': 23, 'Valencia': 61, 'Union': 59,
                    'Bernalillo': 1, 'Lincoln': 27, 'Sierra': 51, 'Sandoval': 43, 'San Juan': 45,
                    'Guadalupe': 19, 'Quay': 37, 'Rio Arriba': 39, 'Taos': 55, 'Mora': 33, 'Roosevelt': 41,
                    'Eddy': 15, 'Harding': 21, 'Los Alamos': 28, 'Dona Ana': 13}
    # counties = []
    print('county codes', geo_df.CountyCode)


    # === make a dictionary of how each county matches its coordinates in the site dataframe ===
    county_match_mask_dict = {}
    # todo - Add the counties from other states.
    for index, county in enumerate(nm_counties.NAME.tolist()):
        print(county)
        poly = nm_counties.loc[index, 'geometry']
        county_match_mask = (geo_df.CountyCode == county_codes[county]) & (geo_df.Coordinates.within(poly))
        county_match_mask_dict[county] = county_match_mask

    # ==== PLOTTING ====
    figure, ax = plt.subplots(1)

    nm_counties.plot(ax=ax)
    co_counties.plot(ax=ax)
    tx_counties.plot(ax=ax)
    az_counties.plot(ax=ax)

    # ax = nm_counties.plot(edgecolor='black')
    # # geo_df.plot(ax=ax, color='red')
    masked_dataframes = []
    inverse_masked_dfs = []
    for index, county in enumerate(nm_counties.NAME.tolist()):
        # print(' this is the county mask\n', county_match_mask_dict[county])
        mask = county_match_mask_dict[county]
        masked_df = geo_df[mask]
        print('masked dataframe\n', masked_df.shape)
        # masked_df.plot(ax=ax)
        masked_dataframes.append(masked_df)

        # inverse
        inv_mask = ~mask
        inv_masked_df = geo_df[inv_mask]
        inverse_masked_dfs.append(inv_masked_df)

    # plot each dataframe mask
    for i in masked_dataframes:
        i.plot(ax=ax, color='red')
    plt.show()

    # this is all the good data
    geo_filtered_df = pd.concat(masked_dataframes)
    print('done. DF shape after geo filtering', geo_filtered_df.shape)

    # output the rejected data to a csv
    geo_rejects = pd.concat(inverse_masked_dfs)
    geo_rejects.to_csv(os.path.join(filter_path, 'geo_rejected.csv'))

    # we remove like 1,000 or so bad sites. That will probably decrease after we include the counties from other states.
    return geo_filtered_df


def parse_sites(sites_path, filtered_data_path, county_paths):
    """"""

    # read in dataframe
    sites_df = pd.read_csv(sites_path)

    # first thing to do is rename the columns of the sites dataframe so they're easier to work with
    sites_df = rename_cols(sites_df)

    # # This is to make the full dataframe display
    # pd.set_option('display.max_columns', None)

    # === get rid of sites with duplicate dates ===
    print('before removing duplicates', sites_df.shape)
    sites_df = sites_df.drop_duplicates('SiteID')
    print('after removing duplicates', sites_df.shape)

    # === separate out sites with incorrect site ID (wrong number of digits) ===
    site_id_len = len('312804108332301')
    site_id_mask = sites_df.SiteID.apply(lambda id: len(str(id))) == site_id_len
    # The sites that don't meet the stardard are output to a file
    sites_df_bad_site_id = sites_df[~site_id_mask]
    print('removed {} bad site ids'.format(sites_df_bad_site_id.shape))
    sites_df_bad_site_id.to_csv(os.path.join(filtered_data_path, 'bad_site_id.csv'))
    # otherwise the sites are removed from our working dataframe
    sites_df = sites_df[site_id_mask]

    # === Query the SQL database to see if there are any new sites ===
    # todo - Get this part going after thanksgiving

    # === Check to make sure that county codes match the lat long coordinates of any of the sites
    sites_df = geo_pandas_parse(sites_df, filtered_data_path, nm_county_path=county_paths['nm'], tx_county_path=county_paths['tx'],
                     co_county_path=county_paths['co'], az_county_path=county_paths['az'])


def main(wl_path, sites_path, county_paths, filteted_data_path):
    """

    :param wl_path:
    :param sites_path:
    :param county_paths:
    :param filteted_data_path:
    :return:
    """

    # process the sites that are erroneous, or badly located or already in the database...
    parse_sites(sites_path, filtered_data_path, county_paths)



if __name__ == "__main__":

    # # format to csv. Only do this once
    # format_to_csv()

    waterlevel_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/2018wls.csv"
    sites_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/2018sites.csv"

    # filtered data path - for outputting rejected data
    filtered_data_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/data_taken_out"


    # paths to shapefiles to geographically parse sites
    nm_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/provision-878783/fe_2007_35_county.shp"
    tx_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/political-bnd_tx/txdot-counties/txdot_2015_county_detailed_tx.shp"
    co_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/Colorado_County_Boundaries/Colorado_County_Boundaries.shp"
    az_county_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/AZ_border_counties/AZ_border_counties.shp"
    # pack the paths into a dictionary for 'portability'
    county_paths = {'nm': nm_county_path, 'tx': tx_county_path, 'co': co_county_path, 'az': az_county_path}

    main(waterlevel_path, sites_path, county_paths, filtered_data_path)