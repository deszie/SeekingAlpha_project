import os
from bs4 import BeautifulSoup

from nlp_core.names_extractor import get_names_from_str_tags_list, list_all_mentioned_names
from nlp_core.words_lists import *
from text_parser.sa_chunks_parser import qa_start_find
from text_parser.utils import read_txt_file_with_decoding, get_list_items_by_index


def _return_n_if_strong_tag(x):
    return x[0] if "<strong>" in x[1] else None

def get_n_strong_tags(p_tags_list):
    p_tags_list_str = list(map(str, p_tags_list))
    enum_p_tags = list(enumerate(p_tags_list_str))

    n_strong_tags = list(map(_return_n_if_strong_tag, enum_p_tags))
    n_strong_tags = list(filter(lambda x: x is not None, n_strong_tags))

    return n_strong_tags



def expand_analysts_executives_list(analysts_executives_list):
    executives = analysts_executives_list["executives"]
    analysts = analysts_executives_list["analysts"]

    executives.append('Unknown Executive')
    executives.append('Unidentified Company Representative')
    executives.append('Unidentified Corporate Participant')

    analysts.append('Unidentified Analyst')

    analysts_executives_list["executives"] = executives
    analysts_executives_list["analysts"] = analysts
    analysts_executives_list["unidentified_participants"] = ['Unknown Attendee']
    return analysts_executives_list








if __name__=="__main__":

    file_path = '../data/txt_data/inner/3309_num_6.txt'
    str_text = read_txt_file_with_decoding(file_path)

    bstext = BeautifulSoup(str_text, 'html.parser')

    list_of_bs_p_tags = bstext('p')

    qa_start = qa_start_find(list_of_bs_p_tags)
    qa_session_p_tags = list_of_bs_p_tags[qa_start:]
    n_strong_tags = get_n_strong_tags(list_of_bs_p_tags)
    strong_tags_after_qa_list = list(filter(lambda x: x>qa_start, n_strong_tags))

    get_list_items_by_index(list_of_bs_p_tags, strong_tags_after_qa_list)

    print()

    # names_p_tags = list(map(lambda x: x.text, list_of_bs_p_tags))
    # names = get_names_from_str_tags_list(names_p_tags)

    # n_names = calc_n_names(names)
    # n_tags_with_name = get_n_one_name_tags(n_names)

    # names_list = list_all_mentioned_names(names)



