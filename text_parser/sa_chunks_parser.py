import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np



def qa_start_find_by_id(list_p_tags):
    QA_begin = None
    for p in range(len(list_p_tags)):
        if list_p_tags[p].get('id') == "question-answer-session":
            QA_begin = p
            break
    return QA_begin

def _compare_qa_string(regex_found):
    compare_res_1 = "".join(regex_found[:4]) == "questionsandanswerssession"
    compare_res_2 = "".join(regex_found[:4]) == "questionandanswersession"
    return compare_res_1 | compare_res_2

def _check_tag_for_QA_text(tag_text):
    regex_found = re.findall(r'[a-z]+', tag_text.lower())
    if len(regex_found)>=4:
        if _compare_qa_string(regex_found):
            return True
    return False

def qa_start_find(list_p_tags):
    QA_begin = qa_start_find_by_id(list_p_tags)
    if QA_begin is None:
        for p in range(len(list_p_tags)):
            t = list_p_tags[p].text
            if _check_tag_for_QA_text(list_p_tags[p].text):
                QA_begin = p
                break
    return QA_begin


def get_names_list_chunks(list_of_bs_p_tags):
    executives_flag = 0
    analysts_flag = 0
    stop_flag = 0
    for p in range(len(list_of_bs_p_tags)):
        if len(list_of_bs_p_tags[p].contents) != 0:
            if 'Executives' in list_of_bs_p_tags[p].text:
                executives_flag = p
            elif '<strong>Executive' in str(list_of_bs_p_tags[p].contents[0]):
                executives_flag = p
            if 'Analysts' in list_of_bs_p_tags[p].text:
                analysts_flag = p
            elif '<strong>Analyst' in str(list_of_bs_p_tags[p].contents[0]):
                analysts_flag = p
            if '<strong>Operator' in str(list_of_bs_p_tags[p].contents[0]):
                stop_flag = p
                break
    return executives_flag, analysts_flag, stop_flag


