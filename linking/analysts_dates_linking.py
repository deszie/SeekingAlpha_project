import os
import pandas as pd
import numpy as np
import re

def preproc_name(s):
    s = re.sub(' +', ' ', s).lower()
    s = s.replace(",", "").replace(".", "").replace("\\", "").replace("/", "").replace("'", "").replace('"', "").replace('’', "")
    return s


def min_max_date(dates_list):
    if len(dates_list)>0:
        return [min(dates_list), max(dates_list)]
    else:
        return [np.nan, np.nan]


# def find_analysts_min_max_dates(anname, files):
#     an_dates = []
#     for file_path in files:
#
#         df = pd.read_excel(file_path)
#
#         if df.shape[0] > 0:
#             an_date_df = df[['Analyst', 'Date_published']].drop_duplicates()
#             an_date_df['Analyst'] = an_date_df.apply(lambda x: preproc_name(x[0]), axis=1)
#
#             an_dates += an_date_df.loc[an_date_df['Analyst'] == anname, "Date_published"].tolist()
#
#     return min_max_date(an_dates)

def find_analysts_min_max_dates(anname, analysts_dates_df):
    an_dates = analysts_dates_df.loc[analysts_dates_df['Analyst'] == anname, "Date_published"].tolist()
    return min_max_date(an_dates)

#####################################################################################################################

wd = "../"

#####################################################################################################################

linking = pd.read_excel(wd + "analysts_linking.xlsx")

linking_all_rules = linking[["SA_Analyst", "SA_Analyst_bank", "recdet_analyst", "recdet_analyst_bank_plus_one_to_one_match", "recdet_bank"]].copy()
linking_all_rules = linking_all_rules.loc[linking_all_rules["recdet_analyst_bank_plus_one_to_one_match"].dropna().index]
linking_all_rules = linking_all_rules.reset_index(drop=True)

#####################################################################################################################

folders = [
    "data/result_tables/described/",
    "data/result_tables_from2264/described/"
]

alltabs = []
for f in folders:
    alltabs += list(map(lambda x: wd + f + x, os.listdir(wd + f)))

anlysts_dates_df_concated = []
for f in alltabs:
    df = pd.read_excel(f)
    print(f)
    if df.shape[0] > 0:
        an_date_df = df[['Analyst', 'Date_published']].drop_duplicates()
        an_date_df['Analyst'] = an_date_df.apply(lambda x: preproc_name(x[0]), axis=1)
        anlysts_dates_df_concated.append(an_date_df)

anlysts_dates_df_concated = pd.concat(anlysts_dates_df_concated)
anlysts_dates_df_concated = anlysts_dates_df_concated.drop_duplicates().reset_index(drop=True)

os.mkdir(wd + "data/dates_linking/")

print(len(linking_all_rules)//25 + 1)

for p in range(len(linking_all_rules)//25 + 1):

    print(p)

    start = p * 25
    end = (p+1) * 25

    cur_link = linking_all_rules.iloc[start:end, :].copy()

    # dates_links = cur_link["SA_Analyst"].apply(lambda x: find_analysts_min_max_dates(x, alltabs))
    dates_links = cur_link["SA_Analyst"].apply(lambda x: find_analysts_min_max_dates(x, anlysts_dates_df_concated))

    cur_link["StartDate"] = dates_links.apply(lambda x: x[0]).tolist()
    cur_link["EndDate"] = dates_links.apply(lambda x: x[1]).tolist()

    cur_link.to_excel(wd + "data/dates_linking/" + "analysts_dates_{}.xlsx".format(p))



# p = 0
#
# start = 25
# end = 26
# cur_link = linking_all_rules.iloc[start:end, :].copy()
#
# dates_links = cur_link["SA_Analyst"].apply(lambda x: find_analysts_min_max_dates(x, alltabs))
#
# cur_link["StartDate"] = dates_links.apply(lambda x: x[0]).tolist()
# cur_link["EndDate"] = dates_links.apply(lambda x: x[1]).tolist()
#
# cur_link.to_excel(wd + "data/dates_linking/" + "analysts_dates_{}.xlsx".format(p))

df_list = []
for df_path in os.listdir(wd + "data/dates_linking/"):
    df = pd.read_excel(wd + "data/dates_linking/" + df_path)
    df_list.append(df)

df_res = pd.concat(df_list)

df_res[['SA_Analyst',
        'SA_Analyst_bank',
        'recdet_analyst',
        'recdet_bank',
        'StartDate',
        'EndDate']].drop_duplicates().reset_index(drop=True).to_excel("analysts_dates_linking.xlsx")






