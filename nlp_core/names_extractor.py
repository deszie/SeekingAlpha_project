import os
from bs4 import BeautifulSoup

from text_parser.utils import read_txt_file_with_decoding, count_words_from_list_in_string
from nlp_core.words_lists import STOP_NAME_WORDS

import spacy
nlpcore = spacy.load('../en_core_web_sm')

def get_persons(text):
    persons_list = []
    nlp_text = nlpcore(text)
    for ent in nlp_text.ents:
        if ent.label_ == "PERSON":
            persons_list.append(ent)
    return persons_list

def get_names_from_str_tags_list(str_tags_list):
    return list(map(get_persons, str_tags_list))

def calc_n_names(names_list):
    return list(map(len, names_list))

def get_n_one_name_tags(calc_n_names_list):
    tuple_name_tags = list(filter(lambda x: x[1]==1, enumerate(calc_n_names_list)))
    return list(map(lambda x: x[0], tuple_name_tags))



def split_by_hyphen(name):
    utf_name = name.encode('utf-8')
    result_list = [name, 'No_info_found']
    if b'\xe2\x80\x93' in utf_name:
        result_list = utf_name.split(b'\xe2\x80\x93')
        result_list = [result_list[0].decode(), result_list[1].decode()]
    elif '-' in name:
        result_list = name.split('-')
    result_list = [result_list[0], ' - '.join(result_list[1:])]
    return list(map(lambda x: x.strip(), result_list))

def get_name_before_hyphen(name):
    name_comp_list = split_by_hyphen(name)
    return name_comp_list[0]






def list_all_mentioned_names(extracted_names_list):
    names_list = list(set(sum(extracted_names_list, [])))
    names_list_text = list(map(lambda x: x.text, names_list))
    names_list_comp_cleaned = list(set(map(get_name_before_hyphen, names_list_text)))

    if "ERRORS" in names_list_comp_cleaned:
        names_list_comp_cleaned.remove("ERRORS")

    return names_list_comp_cleaned




def get_all_mentioned_names(list_of_text_p_tags):
    names = get_names_from_str_tags_list(list_of_text_p_tags)
    names_list = list_all_mentioned_names(names)
    return names_list



def find_first_tag_with_stop_words(p1_tags_text_list):
    stop_word_tag_flag = None
    l = len(p1_tags_text_list)
    for p in range(l):
        words_intersection = count_words_from_list_in_string(p1_tags_text_list[p], STOP_NAME_WORDS)
        if words_intersection>0:
            stop_word_tag_flag = p
            break
    return stop_word_tag_flag








if __name__=="__main__":

    file_path = '../data/txt_data/inner/3032_num_10.txt'
    str_text = read_txt_file_with_decoding(file_path)

    bstext = BeautifulSoup(str_text, 'html.parser')
    list_of_bs_p_tags = bstext('p')

    text_p_tags = list(map(lambda x: x.text, list_of_bs_p_tags))

    names = get_names_from_str_tags_list(text_p_tags)
    names_list = list_all_mentioned_names(names)

    # n_names = calc_n_names(names)
    # n_tags_with_name = get_n_one_name_tags(n_names)

    import time

    start = time.time()
    names_list = get_all_mentioned_names(text_p_tags)
    end = time.time()
    print(end - start)

    print()








