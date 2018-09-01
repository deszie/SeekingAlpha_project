import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np

RESULT_DF_COLUMNS_NAMES = [
        'Company_name',
        'Company_name_tag_a_info',
        'Company_ticker_symbol_tag_a_info',
        'Company_name_regex_find',
        'Company_name_description',
        'Date_published',
        'Date_modified',
        'Date_desc',
        'Analyst',
        'Analyst_bank',
        'Executive',
        'Executive_position',
        'Question',
        'Answer',
        'Q_n_tag',
        'A_n_tag',
        'Analysts_list',
        'Executives_list',
        'SYS_INFO'
    ]

def read_txt_file(file_path):
    text_file = open(file_path, "r")
    str_text = text_file.read()
    text_file.close()
    return str_text

def read_txt_file_with_decoding(file_path):
    with open(file_path, "rb") as f:
        text_file = f.read()
        text_file_decoded = text_file.decode('utf-8', 'ignore')
    return text_file_decoded

def get_text_from_bs_tag(a):
    return a.text

def extract_text_from_tag_list(bs_tag_list):
    return ' '.join(list(map(get_text_from_bs_tag, bs_tag_list)))

def file_is_not_full(bs_text_data, critical_length=7):
    for p in range(len(bs_text_data)):
        if 'question-and-answer session not available' in bs_text_data[p].text.lower():
            return True
        if 'no q&a session for this event' in bs_text_data[p].text.lower():
            return True
    if len(bs_text_data)<=critical_length:
        return True
    return False

def check_string_in_list_strings(s, l):
    if (len(s)>0) & (len(l)>0):
        s_proc = s.lower().replace(" ", "").replace(".", "").replace(",", "")
        for el in l:

            el_proc = el.lower().replace(" ", "").replace(".", "").replace(",", "")

            if s_proc in el_proc:
                return True
    return False

def check_list_strings_in_string(s, l):
    if (len(s)>0) & (len(l)>0):
        s_proc = s.lower().replace(" ", "").replace(".", "").replace(",", "")
        for el in l:

            el_proc = el.lower().replace(" ", "").replace(".", "").replace(",", "")

            if el_proc in s_proc:
                return True
    return False












