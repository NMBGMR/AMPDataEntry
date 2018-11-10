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


def gen_parce(csv_path, site_id, output_data_path):
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
    alt_genchem_list = ["pH", "Conductivity (uS/cm)", "TDS (ppm) (calculation)", "Hardness (CaCO3)",
                        "Bicarbonate (HCO3-)", "Chloride (Cl-)",
                        "Sulfate (SO42-)", "Sodium (Na)", "Potassium (K)",
                        "Magnesium (Mg)", "Calcium (Ca)", "Total epm Cations", "Total epm Anions", "% Difference"]

    # create a dictionary to hold the name and value of the info that we need from our shopping list.
    relevant_rows = {}

    # the minor chem analytes from the database that need to go in a different place
    minor_chem_rows = ["Bromide (Br)", 'Fluoride (F-)', 'Nitrite (NO2-)', 'Nitrate (NO3-)', 'Phosphate (PO43-)']
    minor_rows = {}
    # open the file
    try:
        print('trying to open file at {}'.format(csv_path))
        with open(csv_path, mode='r') as csv:
            # print('file opened')
            for line in csv:

                # get a list of each line with commas and chop off the index
                line = line.split(",")[1:]
                # print("line!", line)

                # now we need to get the correct values from the lists

                if line[0] == "Lab. Number":
                    chemlab_id = line[1]
                    print "chemlab id", chemlab_id

                # we also need to kick out Br, F, NO2, NO3, PO4
                if line[0] in minor_chem_rows:
                    # don't need to worry about rounding if the < is in the minor chem
                    # print("{}".format(line[0]), ' is a minor chem')
                    if "<" in line[1]:
                        print('{}'.format(line[0]), ' has < in it')
                        minor_rows[line[0]] = line[1]

                    elif line[0] in ["Bromide (Br)", 'Nitrite (NO2-)', 'Nitrate (NO3-)', 'Phosphate (PO43-)']:
                        # print('lines 1 and 2', line[0], line[1])
                        raw_val = float(line[1])
                        round_val = round(raw_val, 1)
                        minor_rows[line[0]] = "{}".format(round_val)

                    elif line[0] == 'Fluoride (F-)':
                        # print('{}'.format(line[0]), ' is floride')
                        raw_val = float(line[1])
                        round_val = round(raw_val, 2)
                        minor_rows[line[0]] = "{}".format(round_val)

                if line[0] in list(set().union(genchem_list, alt_genchem_list)):
                    # print('{}'.format(line[0]), ' is indeed in the list')

                    # TODO - handle the rounding here. round(float, ndigits)

                    # if the second column is tds or hardness, we want that value, rounded to the nearest interger
                    if line[0] in ["TDS (ppm) (calculation)", "Hardness (CaCO3)"]:
                        # print('line 0: ', line[0])
                        # print('line 1: ', line[1])
                        # print('line 2: ', line[2])
                        value = float(line[1])
                        round_val = round(value, 0)
                        round_val = int(round_val)
                        relevant_rows[line[0]] = "{}".format(round_val)
                    # if the second column doesn't have a value i.e. total cations, we want the third value rounded to
                    #  two decimal places
                    elif line[0] in ["Total meq/L Cations", "Total meq/L Anions", "Total epm Cations",
                                     "Total epm Anions", "% Difference"]:
                        # print('whats line 2?', line[2])
                        value = float(line[2])
                        round_val = round(value, 2)
                        relevant_rows[line[0]] = round_val
                    # the rest of the values don't seem to need to be rounded
                    elif line[1] != '':
                        relevant_rows[line[0]] = line[1]

            #
            # else:
            #     print('that row was not relevant')

    except Exception as e:
        print("the exception", e)
        print('something has gone wrong')
    #     # sys.exit("shutdown")

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
    print('relevant rows \n', relevant_rows)
    # === make the sample value dictionary ===
    sample_val_list = []
    for index, name in enumerate(genchem_list):
        # get the value from relevant rows
        try:
            rel_value = relevant_rows[name]
        except KeyError:
            print('the key', alt_genchem_list[index])
            rel_value = relevant_rows[alt_genchem_list[index]]
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
            unit = 'uS/cm'
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

    # if output_data_path == None:
    #
    #     pathbegin = csv_path.split(".")[0]
    #     path_end = csv_path.split(".")[1]
    #
    #     new_path = "{}_formatted.{}".format(pathbegin, path_end)
    #
    #     df.to_csv(new_path)
    #
    # else:
    #     pathbegin = csv_path.split(".")[0]
    #     if "/" in pathbegin:
    #         filename = pathbegin.split("/")[-1]
    #     else:
    #         # to handle windows file paths
    #         filename = pathbegin.split("\\")[-1]
    #     fullpath = os.path.join(output_data_path, "{}_formatted.csv".format(filename))
    #     df.to_csv(fullpath)

    # ====== OUTPUTTING =======
    pathbegin = csv_path.split(".")[0]
    if "/" in pathbegin:
        filename = pathbegin.split("/")[-1]
    else:
        # to handle windows file paths
        filename = pathbegin.split("\\")[-1]
    fullpath = os.path.join(output_data_path, "{}_formatted.csv".format(filename))
    df.to_csv(fullpath)

    return chemlab_id, minor_rows


def trace_parce(csv_path, site_id, chemlab_id, minor_rows_gen, output_data_path):
    """"""
    # take care of this section. same approach, just have to deal with two subsets of trace analytes, one thats
    #  on the general chemistry sheet (minor rows gen) and the main one that you'll get out of the trace metals
    # spreasheet that bonnie did. I think if we just do multiple lists subset1, subset2 and then the full set, we'll be
    #  able to get em all out in the correct order.
    # also need to get the < from one row to another...

    full_minor_chem_list = ["Bromide (Br)", 'Fluoride (F-)', 'Nitrite (NO2-)', 'Nitrate (NO3-)', 'Phosphate (PO43-)',
                            "Aluminum (Al)", "Antimony (Sb)", "Arsenic (As)", "Barium (Ba)", "Beryllium (Be)",
                            "Boron (B)",
                            "Cadmium (Cd)", "Chromium (Cr)", "Cobalt (Co)", "Copper (Cu) ", "Iron (Fe)", "Lead (Pb)",
                            "Lithium (Li)", "Manganese (Mn)", "Mercury (Hg)", "Molybdenum (Mo)", "Nickel (Ni)",
                            "Selenium (Se)", "Strontium (Sr)", "Silica (SiO2)   ", "Silicon (Si)", "Silver (Ag)",
                            "Thalium (Tl)", "Thorium (Th)", "Tin (Sn)", "Titanium (Ti)", "Uranium (U)", "Vanadium (V)",
                            "Zinc (Zn)  "]
    minor_chem_partial = ["Bromide (Br)", 'Fluoride (F-)', 'Nitrite (NO2-)', 'Nitrate (NO3-)', 'Phosphate (PO43-)']

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

                if "<" not in line[1] and line[1] != '' and line[0] in full_minor_chem_list:
                    # round some things to one decimal
                    if line[0] in ["Bromide (Br)", 'Nitrite (NO2-)', 'Nitrate (NO3-)', 'Phosphate (PO43-)']:
                        raw_val = float(line[1])
                        round_val = round(raw_val, 1)
                        trace_rows[line[0]] = "{}".format(round_val)

                    # round some things to two decimals
                    elif line[0] in ['Fluoride (F-)', "Iron (Fe)"]:
                        raw_val = float(line[1])
                        round_val = round(raw_val, 2)
                        trace_rows[line[0]] = "{}".format(round_val)

                    # round some to things to an interger
                    elif line[0] in ["Silica (SiO2)   ", "Silicon (Si)"]:
                        raw_val = float(line[1])
                        round_val = round(raw_val, 0)
                        round_val = int(round_val)
                        trace_rows[line[0]] = "{}".format(round_val)

                    # otherwise round to three decimal places
                    else:
                        raw_val = float(line[1])
                        round_val = round(raw_val, 3)
                        trace_rows[line[0]] = "{}".format(round_val)
                # if line[0] in full_minor_chem_list:
                #
                #
                #
                #     # if the second column contains a value, we want that value
                #     #TODO - handle the rounding here? round(float, ndigits)
                #
                #     if line[1] != '':
                #         trace_rows[line[0]] = line[1]
                #         # # if the second column doesn't have a value i.e. total cations, we want the third value
                #         # else:
                #         #     trace_rows[line[0]] = line[2]

                # here we take care in case there is a '< symbol'
                elif line[0] in full_minor_chem_list:
                    if line[1] != '':
                        trace_rows[line[0]] = line[1]

                else:
                    print(line[0], "not in the list")

    except:
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
    col_dict_list = [samplepoint_col_dict, analyte_col_dict, detection_limit_col_dict, sample_col_dict, unit_col_dict,
                     uncertainty_col_dict, analysis_method_col_dict, analysis_date_col_dict, analysis_lab_col_dict,
                     chemlabid_col_dict]

    df = data_frame_formatter(col_dict_list)

    # ====== OUTPUTTING =======
    pathbegin = csv_path.split(".")[0]
    if "/" in pathbegin:
        filename = pathbegin.split("/")[-1]
    else:
        # to handle windows file paths
        filename = pathbegin.split("\\")[-1]
    fullpath = os.path.join(output_data_path, "{}_formatted.csv".format(filename))
    df.to_csv(fullpath)


if __name__ == "__main__":
    """
    for gen chem and for trace chem we parse them according to the input table formats of Major Chem and Minor Chem
     data entry templates
    """

    # for testing
    kolshorn_gen = "Z:\\data\datasets\\TSWCD_Chemistry\\BonniesLabResults\\NotInOurDB" \
                   "\\gabe_temp_geochem\\06-0038_MLC-53_Kolshorn_NoLocation_gen.csv"

    kolshorn_trace = "Z:\\data\datasets\\TSWCD_Chemistry\\BonniesLabResults\\NotInOurDB" \
                     "\\gabe_temp_geochem\\06-0038_MLC-53_Kolshorn_NoLocation_trace.csv"

    output = "Z:\data\datasets\TSWCD_Chemistry\BonniesLabResults\NotInOurDB\gabe_temp_geochem"

    # don't forget the A or B etc if it's the first/second sample from the site, got it?
    site_id = "NM-28308A"
    chemlab_id, minor_rows = gen_parce(kolshorn_gen, site_id, output)
    print('chemlab id', chemlab_id, 'minor rows', minor_rows)

    trace_parce(kolshorn_trace, site_id, chemlab_id, minor_rows, output)


    # #testing formatting on a directory of formatted gen then formatted trace
    # # gen_path = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/copy_paste_test_dir/oc_pil_format_gen"
    #
    # path = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/copy_paste_test_dir/oc_pil_format"
    #
    # # trace_path = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/copy_paste_test_dir/oc_pil_format_trace"
    #
    # # format gen
    # for file in os.listdir(path):
    #     print(file.split(".")[0])
    #     if file.split(".")[0].endswith("gen"):
    #         print('processing')
    #         process_path = os.path.join(path, file)
    #         chemlab_id, minor_rows = gen_parce(process_path, site_id)
    #         trace_file = "{}{}".format(file.split("gen")[0], "trace.csv")
    #         trace_process_path = os.path.join(path, trace_file)
    #         trace_parce(trace_process_path, site_id, chemlab_id, minor_rows)
    #     else:
    #         continue
    #
    # # format trace
