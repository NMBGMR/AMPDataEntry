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

def main():
    """"""

    # todo - User defines the site ID
    ex_site_id = "NM-55555"

    # todo - User defines the location of the file.
    kolshorn = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/" \
               "templatesforgeochemistryfilecopypaste/06-0038_MLC-53_Kolshorn NoLocation.xls"

    # the string of the lab number row
    lab_num = "Lab. Number"

    # A list of strings of the names of the starts of the rows of the general chemistry in the order they appear.
    # genchem_list = ["Lab. Number", "pH", "Conductivity (uS/cm)", "TDS (ppm) (calculation)", "Hardness (CaCO3)",
    #                 "Carbonate (CO32-)", "Bicarbonate (HCO3-)", "Chloride (Cl-)", "Fluoride (F-)", "Nitrite (NO2-)",
    #                 "Nitrate (NO3-)", "Phosphate (PO43-)", "Sulfate (SO42-)", "Sodium (Na)", "Potassium (K)",
    #                 "Magnesium (Mg)", "Calcium (Ca)", "Total meq/L Cations", "Total meq/L Anions", "% Difference"]
    # trace_chem_list = ["Lab. Number", "Aluminum (Al)", "Antimony (Sb)", "Arsenic (As)", "Barium (Ba)", "Beryllium (Be)",
    #                    "Boron (B)", "Cadmium (Cd)", "Chromium (Cr)", "Cobalt (Co)", "Copper (Cu)", "Iron (Fe)",
    #                    "Lead (Pb)", "Lithium (Li)", "Manganese (Mn)", "Mercury (Hg)", "Molybdenum (Mo)", "Nickel (Ni)",
    #                    "Selenium (Se)", "Strontium (Sr)", "Silica (SiO2)", "Silicon (Si)", "Silver (Ag)",
    #                    "Thalium (Tl)", "Thorium (Th)", "Tin (Sn)", "Titanium (Ti)", "Uranium (U)", "Vanadium (V)",
    #                    "Zinc (Zn)"]

    # list the values in the order they appear in the word document for genchem and trace chem:
    genchem_list = ["pH", "Conductivity (uS/cm)", "TDS (ppm) (calculation)", "Hardness (CaCO3)",
                    "Bicarbonate (HCO3-)", "Chloride (Cl-)",
                    "Sulfate (SO42-)", "Sodium (Na)", "Potassium (K)",
                    "Magnesium (Mg)", "Calcium (Ca)", "Total meq/L Cations", "Total meq/L Anions", "% Difference"]


    # Read in the Trace Metals and General Chemistry from the spreadsheet in pandas.
    df_genchem = pd.read_excel(kolshorn, sheet_name="Gen Chem")
    df_trace = pd.read_excel(kolshorn, sheet_name="Trace Metals")

    # print(df_genchem)
    #
    #
    # print(kolshorn)

    # all the data we want is in the first two columns so grab em both and turn em into lists
    # GENCHEM STUFF
    chem_names = df_genchem[df_genchem.columns[0]]
    chem_values = df_genchem[df_genchem.columns[1]]
    # ion_bal_values = pd.DataFrame.dropna(df_genchem[df_genchem.columns[2]]).iloc[-2:]
    ion_bal_values = df_genchem[df_genchem.columns[2]].iloc[58:61]

    # todo - Start here tomorrow. Need to get three ion_bal_values to the end of chem_values dataframe
    # todo - idea - convert one or both to list(s), append the values to the end of one in the correct place. yeah yeah

    # add the ion balance values to the chem_values with concat axis=1
    chem_values = pd.concat([chem_values, ion_bal_values], axis=1)

    # test
    print(chem_values)

    print(ion_bal_values, ', are the ion balance values')

    # get rid of nuls of either conc or name by joining the two columns
    g_chem_names_values = pd.concat([chem_names, chem_values], axis=1)
    # then delete na
    g_chem_names_values = pd.DataFrame.dropna(g_chem_names_values)

    print(g_chem_names_values)
    # # split names and values up again to get the values we want
    # chem_names = df_genchem[g_chem_names_values.columns[0]].to_list()
    # chem_values = df_genchem[g_chem_names_values.columns[1]].to_list()

    # define a rows dictionary
    rows_dict = {}
    for index, row in g_chem_names_values.iterrows():
        # print(row['NEW MEXICO BUREAU OF GEOLOGY AND MINERAL RESOURCES'])
        # print(row['Unnamed: 1'])
        rows_dict["{}".format(row['NEW MEXICO BUREAU OF GEOLOGY AND MINERAL RESOURCES'])] = row['Unnamed: 1']

    print("rows_dictionary \n", rows_dict)

    # # now we can get the rows we want based on our list of items (ignore values we don't want)
    #
    # gen_chem_dictionary = {}
    # for item in genchem_list:
    #     gen_chem_dictionary = rows_dict[item]



    # todo - just get through this so you can do a better job on the trace ones...
    # the relationships between Bonnie Lab Results names and the database insert
    # (only ones that go in Major DB entry form)
    genchem_relational_dictionary = {"Lab. Number": "SamplePoint_ID", "pH": "pHL" , "Conductivity (uS/cm)": "CONDLAB",
                             "TDS (ppm) (calculation)": "TDS", "Hardness (CaCO3)": "HRD", "Bicarbonate (HCO3-)": "HCO3",
                             "Chloride (Cl-)": "Cl", "Sulfate (SO42-)": "SO4", "Sodium (Na)": "Na",
                             "Potassium (K)": "K", "Magnesium (Mg)": "Mg", "Calcium (Ca)": "Ca",
                             "Total meq/L Cations": "TCat", "Total meq/L Anions": "TAn", "% Difference": "IONBAL"}

    # now get the value in the genchem_relational dictionary from the rows_dictionary and store it in

    maj_analyte = []
    sample_val = []
    for value in genchem_list:

        quantity = rows_dict[value]
        sample_val.append(quantity)

        constituent_name = genchem_relational_dictionary[value]
        maj_analyte.append(constituent_name)

    print('major chemistry names \n', maj_analyte, '\n majorchemistry values \n', sample_val)


    # # TRACE METALS STUFF
    # trace_names = df_trace[df_trace.columns[0:1]]
    # # trace_values = df_trace[df_trace.columns[1]]
    #
    # # print(chem_names, '\n', trace_names)
    # trace_chem_list = ["Bromide (Br)", "Fluoride (F-)", "Nitrite (NO2-)", "Nitrate (NO3-)", "Phosphate (PO43-)",
    #                    "Aluminum (Al)", "Antimony (Sb)", "Arsenic (As)", "Barium (Ba)", "Beryllium (Be)",
    #                    "Boron (B)", "Cadmium (Cd)", "Chromium (Cr)", "Cobalt (Co)", "Copper (Cu)", "Iron (Fe)",
    #                    "Lead (Pb)", "Lithium (Li)", "Manganese (Mn)", "Mercury (Hg)", "Molybdenum (Mo)", "Nickel (Ni)",
    #                    "Selenium (Se)", "Strontium (Sr)", "Silica (SiO2)", "Silicon (Si)", "Silver (Ag)",
    #                    "Thalium (Tl)", "Thorium (Th)", "Tin (Sn)", "Titanium (Ti)", "Uranium (U)", "Vanadium (V)",
    #                    "Zinc (Zn)"]



if __name__ == "__main__":
    main()

