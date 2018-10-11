import os
from bs4 import BeautifulSoup
import logging
import traceback
import pandas as pd
import sys
import collections
import re


def _get_bad_replics_num(x):
    return int(re.findall(r'[0-9]+', x)[0])


def fs_xl_from_txt_results_stats_calc(XL_RESULTS_FOLDER):
    xl_files = os.listdir(XL_RESULTS_FOLDER)

    df_list = []
    for file in xl_files:

        print(file)

        df = pd.read_excel(os.path.join(XL_RESULTS_FOLDER, file))
        info_df = df[['Company_name', 'Date_published', 'SYS_INFO']].drop_duplicates()
        df_list.append(info_df)

    joint_df = pd.concat(df_list)

    marked_files_rep_info = joint_df["SYS_INFO"].dropna()
    marked_files_rep_info_list = marked_files_rep_info.apply(_get_bad_replics_num).tolist()
    counter_bad_replics = collections.Counter(marked_files_rep_info_list)

    percent_marked = len(marked_files_rep_info) / len(joint_df)

    def get_year(x):
        return x.year
    years = pd.to_datetime(joint_df['Date_published']).apply(get_year)
    counter = collections.Counter(years)
    return pd.DataFrame(list(counter.items())), \
           percent_marked, \
           pd.DataFrame(list(counter_bad_replics.items()), columns=["bad_rep", "count"]).sort_values("bad_rep")


if __name__=="__main__":

    XL_RESULTS_FOLDER = "../data/xl_results/"

    year_count, percent_marked, bad_replics_count = fs_xl_from_txt_results_stats_calc(XL_RESULTS_FOLDER)

    print()



