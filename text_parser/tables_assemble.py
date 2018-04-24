import pandas as pd
from bs4 import BeautifulSoup
import re
import os
from text_parser.one_text_parser import one_text_reader, names_and_companies_getter

wd = '../'

folders = ['data/inner/',
           'data/outer/1-526/',
           'data/outer/770-1046/',
           'data/outer/1047-1241/',
           'data/outer/1242-1894/',
           'data/outer/1900-2721/']

alltxts = []
for f in folders:
    alltxts += list(map(lambda x: wd + f + x, os.listdir(wd + f)))


for i in range(len(alltxts) // 500 + 1):
    print(i)
    files = alltxts[500 * i:500 * (i + 1)]
    df_list_names = []
    for f in files:
        try:
            df = names_and_companies_getter(f, log_folder=wd+'data/result_tables/')
            df_list_names.append(df)
        except:
            print("error ", f)

    pd.concat(df_list_names).to_excel(wd + 'data/result_tables/names_tables/table{}.xlsx'.format(i))



# for i in range(len(alltxts) // 500 + 1):
#     print(i)
#     files = alltxts[500 * i:500 * (i + 1)]
#     df_list_manual = []
#     df_list_marked = []
#     for f in files:
#         try:
#             df1, df2 = one_text_reader(f, log_folder=wd+'data/result_tables/')
#             df_list_manual.append(df1)
#             df_list_marked.append(df2)
#         except:
#             print(f)
#             with open(wd+'data/result_tables/err.txt', 'a') as file:
#                 file.write(f + '\n')
#
#     pd.concat(df_list_manual).to_excel(wd + 'data/result_tables/described/table{}.xlsx'.format(i))
#     pd.concat(df_list_marked).to_excel(wd + 'data/result_tables/marked/table{}.xlsx'.format(i))
#
#







# folder = '../'
#
# files = os.listdir(folder + 'data/parsing')
#
# df_list = []
# for f in files:
#     try:
#         df_list.append(
#             one_text_reader(folder + 'data/parsing/' + f)
#         )
#     except:
#         print(f)
#         with open(folder + 'err.txt', 'a') as file:
#             file.write(f + '\n')
#
# pd.concat(df_list).to_csv(folder + 'table.csv')
#
# ### save errors files
#
# with open(folder + 'err.txt', 'r') as file:
#     err_files = file.readlines()




