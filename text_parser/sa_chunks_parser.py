import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np



def qa_start_find(bs_text_data):
    QA_begin = None
    for p in range(len(bs_text_data)):
        if bs_text_data[p].get('id') == "question-answer-session":
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


