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
import sys

# ============= local library imports ===========================
def convert(excel_file_path):
    """
    The plan is to convert the excell file into a .csv file, which can be read in by python and processed more easily
    :param excel_file_path: a string indicating the location of the .xls file to be converted
    :return: Output is a .csv file
    """
    s_name = None
    # Read in the Trace Metals and General Chemistry from the spreadsheet in pandas.
    print('working on {}'.format(excel_file_path))
    try:
        df_first_sheet = pd.read_excel(excel_file_path, sheet_name="Gen Chem")
        df_secondary_sheet = pd.read_excel(excel_file_path, sheet_name="Trace Metals")
    except:
        # try:
        df_first_sheet = pd.read_excel(excel_file_path, sheet_name="GENCHEM")
        df_secondary_sheet = pd.read_excel(excel_file_path, sheet_name="QUALITY")
        s_name = "quality"
        # except:
        #     print('a sheet name is spelled incorrectly')
        #     # try:
        #     #     df_first_sheet = pd.read_excel(excel_file_path, sheet_name="GENCHEM")
        #     #     df_secondary_sheet = pd.read_excel(excel_file_path, sheet_name="QUALITY")
        #     sys.exit()

    # separate the path from the .xls extension, get the path sans extension. format as ___.csv
    genchem_nametag = "{}_gen.csv".format(excel_file_path.split(".")[0])

    if s_name == None:
        tracechem_nametag = "{}_trace.csv".format(excel_file_path.split(".")[0])
    elif s_name == "quality":
        tracechem_nametag = "{}_quality.csv".format(excel_file_path.split(".")[0])
    # print(genchem_nametag, "\n", tracechem_nametag)

    # output the files as csv files using pandas to the same directory.
    df_first_sheet.to_csv(genchem_nametag)
    df_secondary_sheet.to_csv(tracechem_nametag)

    print('DONE')

if __name__ == "__main__":

    # # for testing
    # kolshorn = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/" \
    #            "templatesforgeochemistryfilecopypaste/06-0038_MLC-53_Kolshorn NoLocation.xls"
    #
    # convert(kolshorn)

    # testing script on a directory of two files

    raw_data_dir = "Z:\data\datasets\TSWCD_Chemistry\BonniesLabResults\NotInOurDB\gabe_temp_geochem"

    for path, dir, files in os.walk(raw_data_dir, topdown=False):
        # print(path)
        # print(dir)
        print(files)

        for file in files:
            if file.endswith(".xls") or file.endswith(".xlsx"):
                bonnies_data_path = os.path.join(path, file)
                convert(bonnies_data_path)
