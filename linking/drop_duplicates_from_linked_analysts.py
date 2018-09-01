import pandas as pd
import numpy as np
import os
import ast


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
    return 0

def find_all_similar_names(R_Analyst, SA_ListAnalysts):
    similar_names = []
    if not pd.isnull(R_Analyst):
        for saname in SA_ListAnalysts:
            comparison_result = compareNames(saname, R_Analyst)
            if comparison_result==1:
                similar_names.append(saname)
    return similar_names

def zip_dict_by_keys(d1, d2):
    zip = []
    for k in d1.keys():
        zip.append(
            str(d1[k]) + " - " + str(d2[k])
        )
    return zip

def prettify_dicts(d):
    d = ast.literal_eval(d)
    if len(d)>0:
        pretty_dict = zip_dict_by_keys(d["analyst_proc"], d["bank_proc"])
        return ", ".join(pretty_dict)
    else:
        return np.nan

wd = "../"

linked = pd.read_excel(wd + "analysts_one_to_one_match.xlsx")
analysts_names_match = linked[["Analyst", "recdet_analyst_bank_match", "recdet_analyst"]].copy()

analysts_names_match["analysts_names_match"] = analysts_names_match.apply(lambda x: 1 if pd.isnull(x[1]) else np.nan, axis=1)

list_of_sa_names = analysts_names_match["Analyst"].drop_duplicates().tolist()
analysts_names_match["similar_names_from_SA"] = analysts_names_match["recdet_analyst"].apply(lambda x: find_all_similar_names(x, list_of_sa_names))

analysts_names_match["SA_unique_recdet_analysts"] = analysts_names_match["similar_names_from_SA"].apply(lambda x: x[0] if len(x)==1 else np.nan)

final_linkage = pd.concat([
    linked, analysts_names_match.iloc[:,3:]
], axis=1)



final_linkage_prettify = final_linkage[['Analyst', 'Analyst_bank', 'RECDET_link1', 'RECDET_link2', 'RECDET_link3']].copy()
final_linkage_prettify.columns = ['SA_Analyst', 'SA_Analyst_bank', 'RECDET_Bank_link1', 'RECDET_Bank_link2', 'RECDET_Bank_link3']

final_linkage_prettify["recdet_analysts_similar_names"] = final_linkage["link_dict"].apply(prettify_dicts)

final_linkage_prettify = pd.concat([
    final_linkage_prettify,
    final_linkage[['recdet_analyst_bank_match', 'recdet_bank_bank_match', 'recdet_analyst', 'recdet_bank']].copy()
], axis=1)

final_linkage_prettify["similar_names_from_SA"] = final_linkage["similar_names_from_SA"].apply(lambda x: ", ".join(x))


final_linkage_prettify["recdet_analyst_bank_plus_one_to_one_match"] = final_linkage["SA_unique_recdet_analysts"].copy()

final_linkage_prettify.to_excel(wd + "analysts_linking.xlsx")


