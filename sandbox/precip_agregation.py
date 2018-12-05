import pandas as pd
import dateparser
import datetime
import numpy as np

# def csv_parse(csv_file):
#     print'parsing {}'.format(csv_file)
#     with open(csv_file, 'r') as rfile:
#
#         count = 0
#         csv_dict = {}
#         # len_line = len(rfile[0])
#         for line in rfile:
#
#             if count == 0:
#                 header = line.split(',')
#                 header_len = len(header)
#
#                 # make empty lists for each heading
#                 for i, h in enumerate(header):
#                     if i == header_len-1:
#                         print('modifying h', h[:-1])
#                         # change header
#                         header[i] = h[:-1]
#                         # change the h too
#                         h = h[:-1]
#                         csv_dict[h] = []
#                     else:
#                         csv_dict[h] = []
#
#             else:
#                 for i, val in enumerate(line.split(',')):
#                     # put in Nan instead of blank lines
#                     if val == '\n' or val == '':
#                         val = 'NaN'
#                     print('index', i)
#                     csv_dict[header[i]].append(val)
#
#             count += 1
#
#         print('csv dictionary \n', csv_dict)
#         return csv_dict




def parse_human_dates(list_of_dates):
    """"""

    parsed_list = []

    for i in list_of_dates:
        parsed_list.append(dateparser.parse(i))

    print 'parsed list \n', parsed_list
    return parsed_list

def parse_dates(list_of_dates):

    parsed_list = []

    for i in list_of_dates:
        parsed_list.append(datetime.datetime.strptime(i, "%m/%d/%y"))

    print 'pdates parsed list', parsed_list
    return parsed_list


def aggregate_precip(agg_dates, maggie, kelly):
    """"""

    print 'the agg dates \n', agg_dates
    mag_date = maggie[0]
    kel_date = kelly[0]

    mag_precip = maggie[1]
    kel_precip = kelly[1]

    # aggregate maggie
    maggie_agg_list = []

    for i in range(len(agg_dates)):

        if i < len(agg_dates)-1:
            agg_date1 = agg_dates[i]
            agg_date2 = agg_dates[i+1]

            print 'agg date 1 and 2', agg_date1, agg_date2

            # accumulate precip in agg if date is between the start and the end.
            ag = 0
            for md, mp in zip(mag_date, mag_precip):
                if md >= agg_date1 and md < agg_date2:
                    ag += mp

            maggie_agg_list.append(ag)
        else:
            agg_date = agg_dates[i]
            ag = 0
            for md, mp in zip(mag_date, mag_precip):
                if md >= agg_date:
                    ag += mp
            maggie_agg_list.append(ag)


    print 'agg list \n', maggie_agg_list
    period_list = []
    kelly_agg_list = []
    for i in range(len(agg_dates)):

        if i < len(agg_dates)-1:
            agg_date1 = agg_dates[i]
            agg_date2 = agg_dates[i+1]

            # keep track of the period
            period_list.append(agg_date1)

            print 'agg date 1 and 2', agg_date1, agg_date2

            # accumulate precip in agg if date is between the start and the end.
            ag = 0
            for kd, kp in zip(kel_date, kel_precip):
                if kd >= agg_date1 and kd < agg_date2:
                    ag += kp

            kelly_agg_list.append(ag)
        else:
            agg_date = agg_dates[i]
            # keep track of period
            period_list.append(agg_date)
            ag = 0
            for kd, kp in zip(kel_date, kel_precip):
                if kd >= agg_date:
                    ag += kp
            kelly_agg_list.append(ag)


    print 'agg list \n', maggie_agg_list
    print 'kelly_list \n', kelly_agg_list

    print 'period list \n', period_list

    print 'lens ', len(maggie_agg_list), len(kelly_agg_list), len(period_list)

    # return three lists
    return period_list, maggie_agg_list, kelly_agg_list

def write_to_csv(period, maggie, kelly, output_path):
    """"""

    with open(output_path, 'w') as wfile:
        wfile.write('Period, Maggie Aggregated Precip (mm), Kelly Aggregated Precip (mm)\n')

        for p, m, k in zip(period, maggie, kelly):
            wfile.write('{}, {}, {}\n'.format(p, m, k))


def main(usage, maggie_precip, wc_precip, output):
    """"""

    # read in each dataset as pd dataframe
    usage_df = pd.read_csv(usage)
    maggie_precip_df = pd.read_csv(maggie_precip)
    wc_precip_df = pd.read_csv(wc_precip)

    # === get dates from usage df ===
    usage_df_dates = usage_df['Date'].tolist()
    print 'dates \n', usage_df_dates
    udates = []
    for i in usage_df_dates:
        d = i.split('-')
        d_new = '1, {}, {}'.format(d[0], d[1])
        udates.append(d_new)
    # replace text dates with datetimes
    parsed_dates = parse_human_dates(udates)

    # between dates in usage_df_dates, we need to get the cumulative precipitations from maggie_precip and wc_precip
    maggie_d = maggie_precip_df['DATE'].tolist()
    maggie_dates = parse_human_dates(maggie_d)
    maggie_precip= maggie_precip_df['PRCP'].tolist()

    maggie = (maggie_dates, maggie_precip)

    kelly_d = wc_precip_df['DATE'].tolist()
    kelly_dates = parse_human_dates(kelly_d)
    kelly_precip = wc_precip_df['PRCP'].tolist()

    kelly = (kelly_dates, kelly_precip)

    period, m_agg, k_agg = aggregate_precip(parsed_dates, maggie, kelly)

    # output the file
    write_to_csv(period=period, maggie=m_agg, kelly=k_agg, output_path=output)



if __name__ == "__main__":

    # usage path
    mag_wells = 'Z:\data\datasets\magdalena_wells\magdalena_wells_17_18.csv'

    # precip paths
    mag_precip = 'Z:\data\datasets\magdalena_wells\magdalena_kellyranch_weather.csv'
    kelly_precip = 'Z:\data\datasets\magdalena_wells\kellyranch_precip.csv'

    output = 'Z:\data\datasets\magdalena_wells\\aggregatedprecip.csv'

    main(mag_wells, mag_precip, kelly_precip, output)
