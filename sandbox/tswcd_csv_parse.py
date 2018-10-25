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

def make_empty_col_dict(genchem_list, name, lab=False):
    """

    :param genchem_list: the list of general chemistry analytes we want to enter into the database
    :param name: a string which is the name of a column header
    :param lab: optional parameter if you are indicating the lab
    :return:
    """

    if not lab:
        lst = []
        for i in range(len(genchem_list)):
            lst.append('')

        col_dict = {"{}".format(name): lst}

        return col_dict

    else:
        lst = []
        for i in range(len(genchem_list)):
            lst.append('NMBGMR')

        col_dict = {"{}".format(name): lst}

        return col_dict


def data_frame_formatter(lst):
    """
    takes the dictionaries in the order of the list, makes a list of dataframes, which are collated in order into a
    larger dataframe
    :param lst: a list of one key dictionaries representing columns in a future spreadsheet
    :return: formatted dataframe
    """
    # print(lst)
    df_list = []
    for d in lst:
        col = list(d.keys())
        col_dataframe = pd.DataFrame(d, columns=col)
        df_list.append(col_dataframe)

    big = []
    for i in range(len(df_list) + 1):
        if i == 0:
            # print(i)
            df = pd.concat([df_list[i], df_list[i + 1]], axis=1)
            # print('first df')
            big.append(df)
        elif (i + 1) < len(df_list):
            # print(i)
            # print('big index {}'.format(i - 1), 'df_list index {}'.format(i + 1))
            big.append(pd.concat([big[i - 1], df_list[i + 1]], axis=1))
    # pd.set_option('display.max_columns', None)
    # print("BIGGest \n", big[-1].head())
    biggest = big[-1]

    return biggest


def gen_parce(csv_path, site_id):
    """
    Parse through Bonnie's old general chemistry spreadsheets and format the data for entry into MS Access...
    :param csv_path:
    :param site_id:
    :return:
    """

    # create a shopping list of the items we'll want from the spreadsheet. If any of these items are in a given line we
    #  keep the line.

    genchem_list = ["pH", "Conductivity (uS/cm)", "TDS (ppm) (calculation)", "Hardness (CaCO3)",
                    "Bicarbonate (HCO3-)", "Chloride (Cl-)",
                    "Sulfate (SO42-)", "Sodium (Na)", "Potassium (K)",
                    "Magnesium (Mg)", "Calcium (Ca)", "Total meq/L Cations", "Total meq/L Anions", "% Difference"]

    # create a dictionary to hold the name and value of the info that we need from our shopping list.
    relevant_rows = {}

    # the minor chem analytes from the database that need to go in a different place
    minor_chem_rows = ["Bromide (Br)", 'Fluoride (F-)', 'Nitrite (NO2-)', 'Nitrate (NO3-)', 'Phosphate (PO43-)']
    minor_rows = {}
    # open the file
    try:
        with open(csv_path, mode='r') as csv:
            for line in csv:

                # get a list of each line with commas and chop off the index
                line = line.split(",")[1:]
                # print(line)

                # now we need to get the correct values from the lists

                if line[0] == "Lab. Number":
                    chemlab_id = line[1]

                # we also need to kick out Br, F, NO2, NO3, PO4
                if line[0] in minor_chem_rows:
                    minor_rows[line[0]] = line[1]

                if line[0] in genchem_list:

                    # if the second column contains a value, we want that value
                    if line[1] != '':
                        relevant_rows[line[0]] = line[1]
                    # if the second column doesn't have a value i.e. total cations, we want the third value
                    else:
                        relevant_rows[line[0]] = line[2]

    except FileNotFoundError:
        print('sorry, cannot find that file')

    # Now comes the time to think about how we get the correct name for the output format placed in the correct order
    #  in a dataframe or something. Idea: 10 1-column dataframes made from 10 1-key custom dictionaries. Like, for
    #  example: {'Major Analyte': [pHL, CONDLAB, TDS, HRD, HCO3, Cl, SO4, Na, K, Mg, Ca, TCat, Tan, IONBAL]}, then you
    #  convert it to a dataframe in the usual way and when ready, we concatenate along the appropriate axis and add the
    #  details and flourishes we need as we go...

    # === make the sample point id dictionary ===
    id_list = []
    for i in range(len(genchem_list)):
        id_list.append(site_id)
    samplepoint_col_dict = {"Sample Point ID": id_list}
    # print(samplepoint_col_dict)

    # === make the major analyte dictionary (hardcoded because it won't change) ===
    analyte_list = ["pHL", "CONDLAB", "TDS", "HRD", "HCO3", "Cl", "SO4", 'Na', 'K', 'Mg', 'Ca', 'TCat', 'Tan', 'IONBAL']
    analyte_col_dict = {"Major Analyte": analyte_list}

    # === make the symbol dictionary (it's empty) ===
    symbol_col_dict = make_empty_col_dict(genchem_list, "Symbol")
    # print(symbol_col_dict)

    # === make the sample value dictionary ===
    sample_val_list = []
    for name in genchem_list:
        # get the value from relevant rows
        rel_value = relevant_rows[name]
        sample_val_list.append(rel_value)
    sample_val_col_dict = {"Sample Value": sample_val_list}

    # === Make the Units dictionary ===
    units_list = []
    for name in genchem_list:
        print(name)
        if name == "pH":
            unit = "pH"
            units_list.append(unit)
        elif name == "Conductivity (uS/cm)":
            unit = "µS/cm"
            units_list.append(unit)
        elif name == "Total meq/L Cations" or name == "Total meq/L Anions":
            unit = "epm"
            units_list.append(unit)
        elif name == "% Difference":
            unit = '%Diff'
            units_list.append(unit)
        else:
            unit = "mg/L"
            units_list.append(unit)
    units_col_dict = {"Units": units_list}
    # print(units_col_dict)

    # === make uncertainty dictionary ===
    uncertainty_col_dict = make_empty_col_dict(genchem_list, "Uncertainty")

    # ==== make analysis method dictionary ===
    anal_methlist = []
    for analyte in analyte_list:
        if analyte == "TDS":
            anal_methlist.append("Calculation")
        elif analyte == "HRD":
            anal_methlist.append("as CaCO3")
        elif analyte == "HCO3":
            anal_methlist.append("Alkalinity as HCO3")
        else:
            anal_methlist.append('')
    anal_meth_col_dict = {"Analysis Method": anal_methlist}

    # === make analysis date col ===
    analysis_date_col_dict = make_empty_col_dict(genchem_list, "Analysis Date")

    # === Make analysis Lab ===
    anal_lab_col_dict = make_empty_col_dict(genchem_list, "Analysis Lab", lab=True)
    # print(anal_lab_col_dict)

    # === Make chemlab id ===
    chemlab_id_list = []
    for i in range(len(genchem_list)):
        chemlab_id_list.append(chemlab_id)
    chemlabid_col_dict = {"Chem Lab ID": chemlab_id_list}
    # print(chemlabid_col_dict)

    # put the dicts in a list in the order we will concatenate them

    lst_of_col_dictionaries = [samplepoint_col_dict, analyte_col_dict, symbol_col_dict, sample_val_col_dict,
                               units_col_dict, uncertainty_col_dict, anal_meth_col_dict, analysis_date_col_dict,
                               anal_lab_col_dict, chemlabid_col_dict]

    # convert those suckers into dataframes and format them in order
    df = data_frame_formatter(lst_of_col_dictionaries)

    # now we'll output the dataframe to the best location

    pathbegin = csv_path.split(".")[0]
    path_end = csv_path.split(".")[1]

    new_path = "{}_formatted.{}".format(pathbegin, path_end)

    df.to_csv(new_path)

    return chemlab_id, minor_rows


def trace_parce(csv_path, site_id, chemlab_id, minor_rows_gen):
    """"""
    # todo - take care of this section. same approach, just have to deal with two subsets of trace analytes, one thats
    #  on the general chemistry sheet (minor rows gen) and the main one that you'll get out of the trace metals
    # spreasheet that bonnie did. I think if we just do multiple lists subset1, subset2 and then the full set, we'll be
    #  able to get em all out in the correct order.
    # TODO - also need to get the < from one row to another...

    full_minor_chem_list = ["Bromide (Br)", 'Fluoride (F-)', 'Nitrite (NO2-)', 'Nitrate (NO3-)', 'Phosphate (PO43-)',
                            "Aluminum (Al)", "Antimony (Sb)", "Arsenic (As)", "Barium (Ba)", "Beryllium (Be)",
                            "Boron (B)",
                            "Cadmium (Cd)", "Chromium (Cr)", "Cobalt (Co)", "Copper (Cu) ", "Iron (Fe)", "Lead (Pb)",
                            "Lithium (Li)", "Manganese (Mn)", "Mercury (Hg)", "Molybdenum (Mo)", "Nickel (Ni)",
                            "Selenium (Se)", "Strontium (Sr)", "Silica (SiO2)   ", "Silicon (Si)", "Silver (Ag)",
                            "Thalium (Tl)", "Thorium (Th)", "Tin (Sn)", "Titanium (Ti)", "Uranium (U)", "Vanadium (V)",
                            "Zinc (Zn)  "]
    minor_chem_partial = ["Bromide (Br)", 'Fluoride (F-)', 'Nitrite (NO2-)', 'Nitrate (NO3-)', 'Phosphate (PO43-)']

    minor_chem_partial_spreadsheet = ["Aluminum (Al)", "Antimony (Sb)", "Arsenic (As)", "Barium (Ba)", "Beryllium (Be)",
                                      "Boron (B)",
                                      "Cadmium (Cd)", "Chromium (Cr)", "Cobalt (Co)", "Copper (Cu)", "Iron (Fe)",
                                      "Lead (Pb)",
                                      "Lithium (Li)", "Manganese (Mn)", "Mercury (Hg)", "Molybdenum (Mo)",
                                      "Nickel (Ni)",
                                      "Selenium (Se)", "Strontium (Sr)", "Silica (SiO2)", "Silicon (Si)", "Silver (Ag)",
                                      "Thalium (Tl)", "Thorium (Th)", "Tin (Sn)", "Titanium (Ti)", "Uranium (U)",
                                      "Vanadium (V)",
                                      "Zinc (Zn)  "]
    trace_rows = {}
    try:
        with open(csv_path, mode='r') as csv:
            for line in csv:

                # get a list of each line with commas and chop off the index
                line = line.split(",")[1:]
                # print(line)

                # now we need to get the correct values from the lists
                print(line[0], line[1])
                if line[0] == "Lab. Number":
                    chemlab_id = line[1]

                if line[0] in full_minor_chem_list:

                    # if the second column contains a value, we want that value
                    if line[1] != '':
                        trace_rows[line[0]] = line[1]
                    # # if the second column doesn't have a value i.e. total cations, we want the third value
                    # else:
                    #     trace_rows[line[0]] = line[2]
                else:
                    print(line[0], "not in the list")

    except FileNotFoundError:
        print('sorry, cannot find that file')
    # print('tracerows \n', trace_rows)
    # print('trace rows zinc', trace_rows['Zinc (Zn)'])

    # add the minor and trace metal analytes that were on the other excel sheet
    for analyte in minor_chem_partial:
        trace_rows[analyte] = minor_rows_gen[analyte]

    # ********** ***************************** ************
    # ********** Start MAKING the Dictionaries ************
    # ********** ***************************** ************

    # === make the sample point id dictionary ===
    id_list = []
    for i in range(len(full_minor_chem_list)):
        id_list.append(site_id)
    samplepoint_col_dict = {"Sample Point ID": id_list}

    # === make the MINOR analyte dictionary (hardcoded because it won't change) ===
    analyte_list = ["Br", "F", "NO2", "NO3", "PO4", "Al", "Sb", "As", "Ba", "Be", "B", "Cd", "Cr", "Co", "Cu", "Fe",
                    "Pb", "Li", "Mn", "Hg", "Mo", "Ni", "Se", "Sr", "SiO2", "Si", "Ag", "Tl", "Th", "Sn", "Ti", "U",
                    "V", "Zn"]
    analyte_col_dict = {"Minor and Trace Analytes": analyte_list}

    # === make the < (below detection limit column) ===
    detection_limit_list = []
    for analyte in full_minor_chem_list:
        try:
            if trace_rows[analyte][0] == "<":
                detection_limit_list.append("<")
            else:
                detection_limit_list.append('')
        except KeyError:
            detection_limit_list.append('')
        except IndexError:
            print('error occurs with analyte {}'.format(analyte))
            detection_limit_list.append('')
    detection_limit_col_dict = {"Symbol": detection_limit_list}

    # === Make Sample Value list ===
    sample_value_list = []
    for analyte in full_minor_chem_list:
        try:
            if trace_rows[analyte][0] == "<":
                sample_value_list.append(trace_rows[analyte][1:])

            else:
                sample_value_list.append(trace_rows[analyte])
        except KeyError:
            print('this analyte was not found in the spreadsheet {}'.format(analyte))
            sample_value_list.append('')
        except IndexError:
            print('error occurs with analyte {}'.format(analyte))
            sample_value_list.append('')

    print(sample_value_list)
    sample_col_dict = {"Sample Value": sample_value_list}

    # === Make the units list (all values mg/L) ===

    unit_list = []
    for i in range(len(full_minor_chem_list)):
        unit_list.append("mg/L")
    unit_col_dict = {"Units": unit_list}
    print(unit_col_dict)

    # ==== Uncertainty list ===
    uncertainty_col_dict = make_empty_col_dict(full_minor_chem_list, "Uncertainty")

    # === Analysis Method ===
    analysis_method_col_dict = make_empty_col_dict(full_minor_chem_list, "Analysis Method")

    # ==== Analysis Date ====
    analysis_date_col_dict = make_empty_col_dict(full_minor_chem_list, "Analysis Date")

    # ==== Analysis Lab ===
    analysis_lab_col_dict = make_empty_col_dict(full_minor_chem_list, "Analysis Lab", lab=True)

    # === Make chemlab id ===
    chemlab_id_list = []
    for i in range(len(full_minor_chem_list)):
        chemlab_id_list.append(chemlab_id)
    chemlabid_col_dict = {"Chem Lab ID": chemlab_id_list}

    # list the dictionaries in the order they come in the output
    col_dict_list = [samplepoint_col_dict, analyte_col_dict, detection_limit_col_dict, sample_col_dict,
                     uncertainty_col_dict , analysis_method_col_dict, analysis_date_col_dict, analysis_lab_col_dict]

    df = data_frame_formatter(col_dict_list)

    pathbegin = csv_path.split(".")[0]
    path_end = csv_path.split(".")[1]

    new_path = "{}_formatted.{}".format(pathbegin, path_end)

    df.to_csv(new_path)


if __name__ == "__main__":
    """
    for gen chem and for trace chem we parse them according to the input table formats of Major Chem and Minor Chem
     data entry templates
    """

    # for testing
    kolshorn_gen = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/" \
                   "templatesforgeochemistryfilecopypaste/06-0038_MLC-53_Kolshorn NoLocation_gen.csv"

    kolshorn_trace = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/" \
                     "templatesforgeochemistryfilecopypaste/06-0038_MLC-53_Kolshorn NoLocation_trace.csv"

    # todo - don't forget the A or B etc if it's the first/second sample from the site, got it?
    site_id = "NM-28308A"
    chemlab_id, minor_rows = gen_parce(kolshorn_gen, site_id)

    trace_parce(kolshorn_trace, site_id, chemlab_id, minor_rows)
