import os
import pandas as pd
from bs4 import BeautifulSoup

from text_parser.head_info_parser_for_untagged import name_company_split
from text_parser.head_info_parser_for_ae_table import get_ae_dict_rules_based
from text_parser.head_info_parser_for_untagged import head_comp, head_date, header_a_tag_company_name
from text_parser.utils import file_is_not_full



def get_ae_tables(ae_dict):
    a_list = ae_dict["analysts"].copy()
    e_list = ae_dict["executives"].copy()

    analysts = list(map(name_company_split, a_list))
    executives = list(map(name_company_split, e_list))

    df_a = pd.DataFrame(analysts, columns=["name", "company"])
    df_e = pd.DataFrame(executives, columns=["name", "position"])

    return df_a, df_e

def append_company_date_info(df,
                             comp_name_1, comp_name_2, comp_name_3, comp_name_4,
                             date_1, date_2, date_3):
    df["company_name"] = comp_name_1
    df["company_name_tag"] = comp_name_2
    df["company_name_desc"] = comp_name_3
    df["company_ticker"] = comp_name_4
    df["date_mod"] = date_1
    df["date_pub"] = date_2
    df["date_desc"] = date_3
    return df



def main_ae_table_creator(str_text):

    bstext = BeautifulSoup(str_text, 'html.parser')
    list_of_p_tags = bstext("p")

    if file_is_not_full(list_of_p_tags):
        df_a = pd.DataFrame(columns=['name', 'company', 'company_name', 'company_name_tag',
                                     'company_name_desc', 'company_ticker', 'date_mod', 'date_pub',
                                     'date_desc'])
        df_e = pd.DataFrame(columns=['name', 'company', 'company_name', 'company_name_tag',
                                     'company_name_desc', 'company_ticker', 'date_mod', 'date_pub',
                                     'date_desc'])
        return df_e, df_a

    company_name, company_name_tag_a_info, company_ticker = header_a_tag_company_name(bstext)
    company_name_desc = head_comp(bstext)
    date_mod, date_pub, date_desc = head_date(bstext)

    ae_dict = get_ae_dict_rules_based(bstext)
    df_a, df_e = get_ae_tables(ae_dict)

    df_a = append_company_date_info(df_a,
                                    company_name, company_name_tag_a_info, company_name_desc, company_ticker,
                                    date_mod, date_pub, date_desc)
    df_e = append_company_date_info(df_e,
                                    company_name, company_name_tag_a_info, company_name_desc, company_ticker,
                                    date_mod, date_pub, date_desc)
    return df_e, df_a











