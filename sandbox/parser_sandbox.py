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

# ============= local library imports ===========================

def format_to_csv():
    waterlevel_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/NMBGR_20160908.xlsx"
    raw_data = pd.read_excel(waterlevel_path, sheet_name="gw.wls.subf")

    # output to a csv
    output_waterlevel_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/NMBGR_20160908.csv"
    raw_data.to_csv(output_waterlevel_path)

def main():
    """
    We're parsing the water level data as given to NMBGMR as was done by Kitty Pokorny.
    :return:
    """
    # first thing is to read in the file as a pandas dataframe, then we'll start parsing it.
    waterlevel_path = "/Users/Gabe/Desktop/AMP/USGS_parsing_datasets/NMBGR_20160908.csv"

    # raw_data = pd.read_excel(waterlevel_path, sheet_name="gw.wls.subf")
    raw_data = pd.read_csv(waterlevel_path)
    # todo vvvvv
    # 25   C276   Accuracy code <-&&&&&&&-> 23   C237   Water-level below LSD have mixed datatypes

    # print('this is the raw data', raw_data)
    pd.set_option('display.max_columns', None)

    print('data \n', raw_data.iloc[:10, 23])

    # ==== Automated Parsing Steps ====

    # 1) Separate Sites and Water Levels two separate dataframes

    sites_cols = ["1   C001   Site ID (station number)                          ",
                  "3   C900   Station name                                      ",
                  "4   C190   Other identifier                                  ",
                  "5   C008   County code                                       ",
                  "6   C909   Latitude NAD83 in decimal degrees                 ",
                  "7   C910   Longitude NAD83 in decimal degrees                ",
                  "8   C035   Method Lat/Long Determined                        ",
                  "9   C011   Lat/Long accuracy code                            ",
                  "10   C016   Altitude of land surface                          ",
                  "11   C022   Altitude Datum                                    ",
                  "12   C017   Method altitude determined                        ",
                  "13   C018   Altitude accuracy                                 ",
                  "14   C027   Hole depth                                        ",
                  "15   C028   Well depth                                        ",
                  "16   C021   Date well constructed                             ",
                  "17   C023   Primary use of site                               ",
                  "18   C024   Primary use of water                              ",
                  "19   C714   Aquifer code                                      ",
                  "23   C237   Water-level below LSD                             "]
    water_level_cols = [] # todo - to be determined, i think it's all of the dataset

    # sites_df = raw_data["1   C001   Site ID (station number)                          "]
    sites_df = raw_data[sites_cols]

    # 2) For Sites, delete duplicates of USGS IDs

    sites_df = sites_df.drop_duplicates("1   C001   Site ID (station number)                          ")
    print(sites_df, '\n sites df, duplictes removed\n')

    # 2a) For Sites, pull sites that are missing corresponding waterlevels...

    # todo - Check w Kitty: i get 28,404 rows (Kitty P. got 28,625)
    sites_df = sites_df[sites_df["23   C237   Water-level below LSD                             "].notnull()]
    print('sites and waterlevels with no corresponding waterlevel\n', sites_df)

    # 2b) For Sites, pull sites that have coordinates outside of New Mexico

    # 2c) For Sites, pull Sites with null water levels below MP (dry wells)

    # 3) For Water Levels, pull out rows with no water level

    # 4) Remove WL's for sites not in New Mexico or that have no coordinates [using 2b]

    # 5) Remove WL's measured below MP or that are Null

    # 6) Remove WL's that actually are blank and have no WL, that are dry, destroyed, obstructed or are
    #  flowing(artesian)

    # ===== Non Automatic Parsing [Interactive?] ====

    # to be continued...


if __name__ == "__main__":

    # # format to csv. Only do this once
    # format_to_csv()

    main()

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