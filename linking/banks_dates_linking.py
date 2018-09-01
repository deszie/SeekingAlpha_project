import pandas as pd
import os
import numpy as np
import re
import ast
from datetime import datetime

def preproc_name(s):
    s = s.replace(' ', '')
    s = s.replace('.', '')
    s = s.replace(',', '')
    s = s.replace('&', '')
    s = s.replace('-', '')
    s = s.replace(')', '')
    s = s.replace('(', '')
    s = s.replace(']', '')
    s = s.replace('[', '')
    s = s.replace('/', '')
    s = s.replace(':', '')
    s = s.replace(';', '')
    s = s.replace('"', '')
    s = s.replace("'", '')
    s = s.replace('$', '').lower()
    return s

def min_max_date(dates_list):
    if len(dates_list)>0:
        return [min(dates_list), max(dates_list)]
    else:
        return [np.nan, np.nan]

def find_banks_min_max_dates(bname, banks_dates_df):
    an_dates = banks_dates_df.loc[banks_dates_df['Analyst_bank'] == bname, "Date_published"].tolist()
    return min_max_date(an_dates)

########

wd = ""

########

bank_linking = pd.read_excel(wd + "linking/bank_llinking_10_freq_treshold.xlsx")
bank_linking = bank_linking[["SA", "RECDET_link1", "RECDET_link2", "RECDET_link3"]].copy()
index_linking = bank_linking["RECDET_link1"].dropna().index
bank_linking = bank_linking.loc[index_linking,:].reset_index(drop=True)

bank_linking["SA"] = bank_linking["SA"].apply(preproc_name)

########

# for csvf in os.listdir(wd + "data/result_tables_old_version/"):
#     print(csvf)
#     df = pd.read_csv(wd + "data/result_tables_old_version/" + csvf)
#     df.to_excel("data/result_tables_old_version_xlsx/" + csvf.replace(".csv", ".xlsx"))


folders = [
    "data/result_tables/described/",
    "data/result_tables_from2264/described/",
    # "data/result_tables_old_version_xlsx/"
]

alltabs = []
for f in folders:
    alltabs += list(map(lambda x: wd + f + x, os.listdir(wd + f)))



banks_dates_df_concated = []
for f in alltabs:
    df = pd.read_excel(f)
    print(f)
    if df.shape[0] > 0:
        b_date_df = df[['Analyst_bank', 'Date_published']].dropna().drop_duplicates()

        try:
            from_list_df = df[['Date_published', "Analysts_list"]].dropna().drop_duplicates()
            from_list_df["Analysts_list"] = from_list_df["Analysts_list"].apply(lambda x: list(ast.literal_eval(x).values()))
            middle_df_series = from_list_df.apply(lambda x: list(map(lambda y: [x[0], y], x[1])), axis=1)

            for mdflist in middle_df_series.tolist():
                b_date_df = pd.concat([
                    b_date_df,
                    pd.DataFrame(mdflist, columns=['Date_published', 'Analyst_bank'])[['Analyst_bank', 'Date_published']]
                ])

            print(1)

        except:
            pass

        b_date_df['Analyst_bank'] = b_date_df.apply(lambda x: preproc_name(x[0]), axis=1)
        banks_dates_df_concated.append(b_date_df)

banks_dates_df_concated = pd.concat(banks_dates_df_concated)
banks_dates_df_concated = banks_dates_df_concated.drop_duplicates().reset_index(drop=True)

# os.mkdir(wd + "data/dates_linking_banks/")

print(len(bank_linking)//25 + 1)

for p in range(len(bank_linking)//25 + 1):

    print(p)

    start = p * 25
    end = (p+1) * 25

    cur_link = bank_linking.iloc[start:end, :].copy()

    dates_links = cur_link["SA"].apply(lambda x: find_banks_min_max_dates(x, banks_dates_df_concated))

    cur_link["StartDate"] = dates_links.apply(lambda x: x[0]).tolist()
    cur_link["EndDate"] = dates_links.apply(lambda x: x[1]).tolist()

    cur_link.to_excel(wd + "data/dates_linking_banks/" + "banks_dates_{}.xlsx".format(p))


df_list = []
for df_path in os.listdir(wd + "data/dates_linking_banks/"):
    df = pd.read_excel(wd + "data/dates_linking_banks/" + df_path)
    df_list.append(df)

df_res = pd.concat(df_list)

df_res.to_excel(wd + "banks_dates_linking.xlsx")


# an_dates = pd.read_excel(wd + "analysts_dates_linking.xlsx")
#
# def find_bank_from_analysts_dates(bname, df_analysts):
#     needed_bank_index = df_analysts.apply(lambda x: True if x[1]==bname else False, axis=1)
#     startdates = df_analysts.loc[needed_bank_index, "StartDate"].tolist()
#     enddates = df_analysts.loc[needed_bank_index, "EndDate"].tolist()
#     return min_max_date(startdates + enddates)
#
# dates_from_analysts = df_res.loc[pd.isnull(df_res["StartDate"]), "SA"].apply(lambda x: find_bank_from_analysts_dates(x, an_dates))
#


df_res = df_res.drop_duplicates()

df_res_cutted = df_res[~pd.isnull(df_res["StartDate"])].reset_index(drop=True)

df_res_cutted.to_excel("bank_dates_linking.xlsx")

