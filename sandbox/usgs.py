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
import os
from pandas import read_csv

from backend.database_connector import DatabaseConnector

SITE_ID_LEN = len('312804108332301')
COUNTY_CODES = {'McKinley': 31, 'Socorro': 53, 'Colfax': 7, 'Cibola': 6, 'Catron': 3,
                'Torrance': 57,
                'Lea': 25, 'Grant': 17, 'San Miguel': 47, 'Otero': 35, 'Santa Fe': 49, 'De Baca': 11,
                'Luna': 29, 'Chaves': 5, 'Curry': 9, 'Hidalgo': 23, 'Valencia': 61, 'Union': 59,
                'Bernalillo': 1, 'Lincoln': 27, 'Sierra': 51, 'Sandoval': 43, 'San Juan': 45,
                'Guadalupe': 19, 'Quay': 37, 'Rio Arriba': 39, 'Taos': 55, 'Mora': 33, 'Roosevelt': 41,
                'Eddy': 15, 'Harding': 21, 'Los Alamos': 28, 'Dona Ana': 13}


def get_bounding_box(poly):
    # get list of points the make up poly
    # pts = poly.points
    # pts = (x1,y1),(x2,y2)...

    xs, ys = zip(*pts)
    return min(xs), max(xs), min(ys), max(ys)


def within(poly, lon, lat):
    # get bounding box
    xmin, xmax, ymin, ymax = get_bounding_box(poly)
    return xmin < lon <= xmax and ymin < lat < ymax


def geo_test(site, nm_counties):
    lon, lat = site['Longitude'], site['Latitude']
    for index, county in nm_counties:
        poly = county['geometry']
        if within(poly, lon, lat) and site['CountyCode'] == county['Name']:
            return True


def clean_sites(root, site_filename):
    counties = make_county_paths(root)

    path = os.path.join(root, site_filename)

    sites_df = read_csv(path)
    sites_df = rename_cols(sites_df)

    # how does this get rid of sites with duplicate dates?
    # === get rid of sites with duplicate dates ===
    print('before removing duplicates', sites_df.shape)
    sites_df = sites_df.drop_duplicates('SiteID')
    print('after removing duplicates', sites_df.shape)

    removed_sites = []
    existing_sites = []
    invalid_geo_sites = []
    valid_sites = []

    db = get_database()

    nm_counties = geopandas.read_file(counties['nm'])

    for row in sites_df:
        siteid = row['SiteID']
        if len(siteid) != SITE_ID_LEN:
            print('removing {}'.format(siteid))
            removed_sites.append(siteid)
        else:
            # test if in database
            dbsite = db.get_site(siteid)
            if dbsite is not None:
                existing_sites.append(siteid)

                # test geo
                if not geo_test(row, nm_counties):
                    invalid_geo_sites.append(siteid)
                else:
                    valid_sites.append(siteid)

    # save removed
    save_list(removed_sites, os.path.join(root, 'removed_sites.csv'))
    save_list(existing_sites, os.path.join(root, 'existing_sites.csv'))
    save_list(invalid_geo_sites, os.path.join(root, 'invalid_geo_sites.csv'))
    save_list(valid_sites, os.path.join(root, 'valid_sites.csv'))
    return existing_sites, removed_sites


# utility functions
def rename_cols(df):
    # get rid of the index column
    # df = df.drop(labels=['Unnamed: 0'], axis=1)

    cols = df.columns.tolist()
    cols = [col.strip().replace(' ', '') for col in cols]
    cols = [col.split('C')[-1][3:] for col in cols]

    print('columns \n', cols)

    # # based on cols, we hardcode new site names which are easier to reference and don't have all kinds of annoying
    # space
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


def save_list(ls, path, delimiter=','):
    with open(path, 'w') as wfile:
        for row in ls:
            line = [str(i) for i in row]
            line = '{}\n'.format(delimiter.join(line))
            wfile.write(line)


def make_county_paths(root):
    # paths to shapefiles to geographically parse sites
    # pack the paths into a dictionary for 'portability'
    args = (('nm', 'provision-878783/fe_2007_35_county.shp'),
            ('tx', 'political-bnd_tx/txdot-counties/txdot_2015_county_detailed_tx.shp'),
            ('co', 'Colorado_County_Boundaries/Colorado_County_Boundaries.shp'),
            ('az', 'AZ_border_counties/AZ_border_counties.shp'))
    return {k: os.path.join(root, v) for k, v in args}


def get_database():
    db = DatabaseConnector()
    db.credentials.username = os.environ['NM_AQUIFER_USERNAME']
    db.credentials.password = os.environ['NM_AQUIFER_PASSWORD']
    db.credentials.host = os.environ['NM_AQUIFER_HOST']
    db.credentials.database_name = 'NM_AQUIFER'

    return db


def main():
    # define some paths
    root = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets"

    es, rms = clean_sites(root, '2018sites.csv')


if __name__ == '__main__':
    main()
# ============= EOF =============================================
