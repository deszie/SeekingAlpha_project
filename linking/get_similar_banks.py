import pandas as pd
import os

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

wd = ""

bank_linking = pd.read_excel(wd + "linking/bank_llinking_10_freq_treshold.xlsx")
bank_linking = bank_linking[["SA", "RECDET_link1", "RECDET_link2", "RECDET_link3"]].copy()
index_linking = bank_linking["RECDET_link1"].dropna().index
bank_linking = bank_linking.loc[index_linking,:].reset_index(drop=True)

bank_linking["SA"] = bank_linking["SA"].apply(preproc_name)


similar_banks = []
for b in pd.unique(bank_linking["RECDET_link1"]):
    sa_b = pd.unique(bank_linking.loc[bank_linking["RECDET_link1"]==b, "SA"]).tolist()
    similar_banks.append(
        [b] + sa_b
    )

similar_banks_df = pd.DataFrame(similar_banks)
similar_banks_df.columns = ["RECDET_ID"] + ["SA_NAME_{}".format(i) for i in range(len(similar_banks_df.columns)-1)]

similar_banks_df.to_excel("banks_names_variants.xlsx")



recdet = pd.read_stata('data/recdet.dta')
recdet_analysts = recdet[["analyst", "estimid"]].drop_duplicates().copy()

recdet[recdet["estimid"]=="FAHN"].to_excel("fahn_recdet.xlsx")

recdet[recdet["cname"]=="JPMORGAN"]

recdet.to_excel("recdet.xlsx")

