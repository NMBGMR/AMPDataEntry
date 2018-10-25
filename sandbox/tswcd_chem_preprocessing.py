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
def convert(excel_file_path):
    """
    The plan is to convert the excell file into a .csv file, which can be read in by python and processed more easily
    :param excel_file_path: a string indicating the location of the .xls file to be converted
    :return: Output is a .csv file
    """

    # Read in the Trace Metals and General Chemistry from the spreadsheet in pandas.
    df_genchem = pd.read_excel(excel_file_path, sheet_name="Gen Chem")
    df_trace = pd.read_excel(excel_file_path, sheet_name="Trace Metals")

    # separate the path from the .xls extension, get the path sans extension. format as ___.csv
    genchem_nametag = "{}_gen.csv".format(excel_file_path.split(".")[0])
    tracechem_nametag = "{}_trace.csv".format(excel_file_path.split(".")[0])
    print(genchem_nametag, "\n", tracechem_nametag)

    # output the files as csv files using pandas to the same directory.
    df_genchem.to_csv(genchem_nametag)
    df_trace.to_csv(tracechem_nametag)

    print('DONE')


if __name__ == "__main__":

    # for testing
    kolshorn = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/" \
               "templatesforgeochemistryfilecopypaste/06-0038_MLC-53_Kolshorn NoLocation.xls"

    convert(kolshorn)
