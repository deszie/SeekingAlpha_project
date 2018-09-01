import pandas as pd
import os
import numpy as np
import re
import ast
from datetime import datetime

def preproc_names_list(l):
    l = list(map(lambda x: x.replace(' ', ''), l))
    l = list(map(lambda x: x.replace('.', ''), l))
    l = list(map(lambda x: x.replace(',', ''), l))
    l = list(map(lambda x: x.replace('&', ''), l))
    l = list(map(lambda x: x.replace('-', ''), l))
    l = list(map(lambda x: x.replace(')', ''), l))
    l = list(map(lambda x: x.replace('(', ''), l))
    l = list(map(lambda x: x.replace(']', ''), l))
    l = list(map(lambda x: x.replace('[', ''), l))
    l = list(map(lambda x: x.replace('/', ''), l))
    l = list(map(lambda x: x.replace(':', ''), l))
    l = list(map(lambda x: x.replace(';', ''), l))
    l = list(map(lambda x: x.replace('"', ''), l))
    l = list(map(lambda x: x.replace("'", ''), l))
    l = list(map(lambda x: x.replace('$', '').lower(), l))
    # if '' in l:
    #     l.remove('')
    return l#pd.unique(l).tolist()

def compareNames(aname, rname):
    '''
    Compare two names from recdet and SA
    :param aname: analyst from SA
    :param rname: analyst from Recdet
    :return:
    '''
    aname_list = aname.split(" ")
    rname_list = rname.split(" ")
    rlettername = rname_list[-1]
    rsurname = rname_list[:-1]

    for a in aname_list:
        for r in rsurname:
            if a==r:
                aname_list.remove(a)
                for a_ in aname_list:
                    if a_[0]==rlettername:
                        return 1
    return np.nan

def find_analysts_dict(aname, recdet_list):
    '''
    Find all analysts from Recdet with surname and name letter in SA
    :param aname: analyst from SA
    :param recdet_list: Recdet DF
    :return:
    '''
    recdet_list = recdet_list.copy()
    coincidences = recdet_list.apply(lambda x: compareNames(aname, x[0]), axis=1)
    recdet_list["ind"] = coincidences
    return recdet_list.dropna().to_dict()

def find_in_dict(d, findlist):
    for v in d.items():
        if v[1] in findlist:
            return v[0]
        else:
            return np.nan

def get_ranalyst(d, findlist):
    aid = find_in_dict(d["bank_proc"], findlist)
    if not pd.isnull(aid):
        return d["analyst_proc"][aid]
    else:
        return np.nan

def get_rbank(d, findlist):
    aid = find_in_dict(d["bank_proc"], findlist)
    if not pd.isnull(aid):
        return d["bank_proc"][aid]
    else:
        return np.nan

def get_ranalyst_plus_one_to_one_match(d, findlist):
    bank_match = get_ranalyst(d, findlist)
    if pd.isnull(bank_match):
        if len(d['analyst_proc'].values())==1:
            return list(d['analyst_proc'].values())[0]
        else:
            return np.nan
    else:
        return bank_match

def get_rbank_plus_one_to_one_match(d, findlist):
    bank_match = get_rbank(d, findlist)
    if pd.isnull(bank_match):
        if len(d['analyst_proc'].values())==1:
            return list(d['bank_proc'].values())[0]
        else:
            return np.nan
    else:
        return bank_match

########

wd = "../"

########

linking = pd.read_excel(wd + "linking/bank_llinking_10_freq_treshold.xlsx")
linking = linking[["SA", "RECDET_link1", "RECDET_link2", "RECDET_link3"]].copy()
index_linking = linking["RECDET_link1"].dropna().index
linking = linking.loc[index_linking,:].reset_index(drop=True)

########

recdet = pd.read_stata(wd + 'data/recdet.dta')
recdet_analysts = recdet[["analyst", "estimid"]].drop_duplicates().copy()
recdet_analysts["bank_proc"] = preproc_names_list(recdet_analysts["estimid"].tolist())
recdet_analysts["analyst_proc"] = recdet_analysts["analyst"].apply(
    lambda x:
    re.sub(' +', ' ', x).lower().replace(",","").replace(".","").replace("\\","").replace("/","").replace("'","").replace('"',"").replace('’',""))
recdet_analysts = recdet_analysts[["analyst_proc", "bank_proc"]].copy()

########

path_to_files_1 = wd + "data/result_tables/described/"
files_part_1 = os.listdir(path_to_files_1)
files_part_1 = list(map(lambda x: path_to_files_1+x, files_part_1))

path_to_files_2 = wd + "data/result_tables_from2264/described/"
files_part_2 = os.listdir(path_to_files_2)
files_part_2 = list(map(lambda x: path_to_files_2+x, files_part_2))

files = files_part_1 + files_part_2

full_df_analyst = []
for f in files:
    df = pd.read_excel(f)
    df_analysts = df[["Analyst", "Analyst_bank", "Analysts_list", "File_path"]].copy()
    df_analysts = df_analysts.drop_duplicates()
    full_df_analyst.append(df_analysts)

full_df_analyst = pd.concat(full_df_analyst)
full_df_analyst = full_df_analyst[["Analyst", "Analyst_bank"]].drop_duplicates()
full_df_analyst = full_df_analyst.fillna("")
full_df_analyst["Analyst_bank"] = preproc_names_list(full_df_analyst["Analyst_bank"].tolist())
full_df_analyst["Analyst"] = full_df_analyst["Analyst"].apply(
    lambda x:
    re.sub(' +', ' ', x).lower().replace(",","").replace(".","").replace("\\","").replace("/","").replace("'","").replace('"',"").replace('’',""))

#######

sa_linked = pd.merge(full_df_analyst,
                     linking,
                     left_on="Analyst_bank",
                     right_on="SA",
                     how="left")
sa_linked = sa_linked.drop_duplicates()
sa_linked = sa_linked.reset_index(drop=True)

sa_linked["Analyst"] = sa_linked["Analyst"].apply(str)
recdet_analysts["analyst_proc"] = recdet_analysts["analyst_proc"].apply(str)

print(len(sa_linked))



for i in range(len(sa_linked) // 500 + 1):
    start_index = i*500
    end_index = (i+1)*500

    nowt = datetime.now()
    print("--- ", nowt)
    sa_part = sa_linked.iloc[start_index:end_index,:].copy()
    dict_link = sa_part[["Analyst"]].apply(lambda x: find_analysts_dict(x[0], recdet_analysts), axis=1)
    sa_part["link_dict"] = dict_link

    sa_part["recdet_analyst_bank_match"] = sa_part.apply(
        lambda x: get_ranalyst(x[6], [x[3], x[4], x[5]]), axis=1)
    sa_part["recdet_bank_bank_match"] = sa_part.apply(
        lambda x: get_rbank(x[6], [x[3], x[4], x[5]]), axis=1)
    sa_part["recdet_analyst"] = sa_part.apply(
        lambda x: get_ranalyst_plus_one_to_one_match(x[6], [x[3], x[4], x[5]]), axis=1)
    sa_part["recdet_bank"] = sa_part.apply(
        lambda x: get_rbank_plus_one_to_one_match(x[6], [x[3], x[4], x[5]]), axis=1)

    print(start_index, end_index, datetime.now() - nowt)

    sa_part.to_excel(wd + "data/linking_results/" + "linked_analysts_" + str(start_index) + "_" + str(end_index) + ".xlsx")



df_list_result = []
for i in range(46):
    start_index = i*500
    end_index = (i+1)*500

    df = pd.read_excel(wd + "data/linking_results/" + "linked_analysts_" + str(start_index) + "_" + str(end_index) + ".xlsx")
    index_recdet = df["recdet_analyst"].dropna().index
    df_add = df.loc[index_recdet].copy()

    df_list_result.append(df_add)


result = pd.concat(df_list_result)

print(len(result))

result = result.reset_index(drop=True)

result.to_excel(wd + "analysts_one_to_one_match.xlsx")


#######################################################################################################################
wd = ''


unmatched = []
for i in range(len(sa_linked) // 500 + 1):
    start_index = i*500
    end_index = (i+1)*500

    sa_part = pd.read_excel(wd + "data/linking_results/" + "linked_analysts_" + str(start_index) + "_" + str(end_index) + ".xlsx")

    sa_part_unmatched = sa_part.loc[pd.isnull(sa_part["recdet_analyst"])][["Analyst", "Analyst_bank"]].drop_duplicates()

    unmatched.append(sa_part_unmatched)

unmatched = pd.concat(unmatched)
unmatched = unmatched.reset_index(drop=True)

unmatched.to_excel("unmatched_analysts.xlsx")

statistics = []
for b in pd.unique(unmatched["Analyst_bank"]):
    statistics.append(
        [b, len(unmatched[unmatched["Analyst_bank"]==b])]
    )

statistics = pd.DataFrame(statistics, columns=["SA_Bank", "Number_of_unmatched_analysts"])

statistics = statistics.sort_values("Number_of_unmatched_analysts", ascending=False).reset_index(drop=True)

statistics = statistics.dropna()

statistics.to_excel("statistics.xlsx")

