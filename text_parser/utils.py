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
    return a.text.strip()

def extract_text_from_tag_list(bs_tag_list):
    return ' '.join(list(map(get_text_from_bs_tag, bs_tag_list)))

def file_is_not_full(list_of_p_tags, critical_length=7):
    for p in range(len(list_of_p_tags)):
        if 'question-and-answer session not available' in list_of_p_tags[p].text.lower():
            return True
        if 'no q&a session for this event' in list_of_p_tags[p].text.lower():
            return True
    if len(list_of_p_tags)<=critical_length:
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

def get_list_items_by_index(list_, indexs):
    return list(map(list_.__getitem__, indexs))

def get_numbers_between_interval(list_, l, u):
    return list(filter(lambda x: (x>=l) & (x<u), list_))




def count_emerging_words(string, word_list):
    return sum(map(lambda x: 1 if x in string else 0, word_list))



def count_words_from_list_in_string(string, words_list):
    string_lower = string.lower()
    string_word_list = re.findall(pattern=r'[a-z]+', string=string_lower)

    set_string_word_list = set(string_word_list)
    set_words_list = set(words_list)
    intersection = list(set.intersection(set_string_word_list, set_words_list))

    return len(intersection)


def count_strings_words_intersection(string1, string2):
    s1_words = re.findall(r'[a-z]+', string1.lower())
    s2_words = re.findall(r'[a-z]+', string2.lower())
    return len(set.intersection(set(s1_words), set(s2_words)))





if __name__=="__main__":
    s1 = "a b c d"
    s2 = "a g . k  - d"
    print(count_strings_words_intersection(s1, s2))





