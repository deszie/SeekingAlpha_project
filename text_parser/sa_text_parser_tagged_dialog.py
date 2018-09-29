import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np

from text_parser.utils import *
from text_parser.head_info_parser import *



def is_tagged(bs_text, n_qa_threshold=0):
    n_qas = len(bs_text.find_all("span", attrs={"class": "question"})) + \
            len(bs_text.find_all("span", attrs={"class": "answer"}))
    if n_qas>n_qa_threshold:
        return True
    else:
        return False



def _return_order_or_none(enum_p_tag):
    if "<strong>Operator" in enum_p_tag[1]:
        return enum_p_tag[0]
    else:
        return None

def get_operator_tags_order(list_of_bs_p_tags):
    p_tags_str = list(map(str, list_of_bs_p_tags))
    enum_p_tags = list(enumerate(p_tags_str))
    operator_order_appear_or_none = list(map(_return_order_or_none, enum_p_tags))
    operator_order_appear = filter(lambda x: x is not None, operator_order_appear_or_none)
    return list(operator_order_appear)



def get_questions_text(bstext):
    bsqs = bstext.find_all("span", attrs={"class": "question"})
    str_q_list = list(map(str, bsqs))
    return str_q_list

def get_answers_text(bstext):
    bsqs = bstext.find_all("span", attrs={"class": "answer"})
    str_a_list = list(map(str, bsqs))
    return str_a_list

def _return_order_or_none_for_given_content(enum_tag_text, content_list):
    # if enum_tag_text[1] in content_list:
    if check_list_strings_in_string(enum_tag_text[1], content_list):
        return enum_tag_text[0]
    else:
        return None

def get_p_tags_order_with_given_text(list_of_bs_p_tags, content_list):
    p_tags_text = list(map(str, list_of_bs_p_tags))
    enum_p_tags = list(enumerate(p_tags_text))
    content_order_appear_or_none = list(map(lambda x: _return_order_or_none_for_given_content(x, content_list), enum_p_tags))
    content_order_appear = filter(lambda x: x is not None, content_order_appear_or_none)
    return list(content_order_appear)



def get_q_a_operator_order_dict(bstext, list_of_bs_p_tags):
    operators_p_tags_order = get_operator_tags_order(list_of_bs_p_tags)

    questions = get_questions_text(bstext)
    q_p_tags_order = get_p_tags_order_with_given_text(list_of_bs_p_tags, questions)

    answers = get_answers_text(bstext)
    a_p_tags_order = get_p_tags_order_with_given_text(list_of_bs_p_tags, answers)

    return {"operator_order_list":operators_p_tags_order,
            "questions_order_list":q_p_tags_order,
            "answers_order_list":a_p_tags_order}



def set_qa_order(q_list, a_list):
    order_structure = []
    n_q = len(q_list)
    for i in range(n_q-1):
        respective_answers = list(filter(lambda x: (x>q_list[i]) & (x<q_list[i+1]), a_list))
        if len(respective_answers)==0:
            respective_answers = [None]
        order_structure += list(zip([q_list[i]] * len(respective_answers), respective_answers))

    last_element = max(q_list+a_list)

    if last_element in a_list:
        respective_answers = list(filter(lambda x: (x>q_list[-1]), a_list))
        order_structure += list(zip([q_list[-1]]*len(respective_answers), respective_answers))
    elif last_element in q_list:
        order_structure.append(tuple([q_list[-1], None]))
    else:
        raise ValueError("Number outside answer and questin lists "
                         "was set as a last element in both lists.")
    return list(zip(*order_structure))



def get_start_end_of_phrase(participant_order, q_a_operator_order_dict):
    if participant_order is None:
        return 0, 0
    oper_order = q_a_operator_order_dict["operator_order_list"]
    q_order = q_a_operator_order_dict["questions_order_list"]
    a_order = q_a_operator_order_dict["answers_order_list"]
    all_phrases_heads = sorted(oper_order + q_order + a_order)

    if participant_order not in all_phrases_heads:
        raise ValueError("Participant tag number is outside possible numbers.")

    # If the participant order has the last phrase,
    # than we take one tag after participant order
    start = participant_order + 1
    if participant_order==all_phrases_heads[-1]:
        end = participant_order+2
    else:
        end = sorted(filter(lambda x: x>participant_order, all_phrases_heads))[0]

    return start, end



def extract_phrase(participant_head_order, q_a_operator_order_dict, list_of_bs_p_tags):
    cur_start, cur_end = get_start_end_of_phrase(participant_head_order, q_a_operator_order_dict)
    phrase_bs_tags = list_of_bs_p_tags[cur_start:cur_end]
    return extract_text_from_tag_list(phrase_bs_tags)


def extract_tagged_names(tag_p_order, list_of_bs_p_tags):
    if tag_p_order is not None:
        name_company = list_of_bs_p_tags[tag_p_order].text
        person_name, person_desc = name_company_split(name_company)
        return person_name, person_desc
    else:
        return None, None



def extract_dialog_info_with_eao_dict(q_a_operator_order_dict, list_of_bs_p_tags):
    questions_n_p_tag, answers_n_p_tag = q_a_operator_order_dict["questions_order_list"], q_a_operator_order_dict["answers_order_list"]

    q_n_p_tag_tuple_structured_order, a_n_p_tag_tuple_structured_order = set_qa_order(questions_n_p_tag, answers_n_p_tag)
    q_n_p_tag_tuple_structured_order_column = list(q_n_p_tag_tuple_structured_order)
    a_n_p_tag_tuple_structured_order_column = list(a_n_p_tag_tuple_structured_order)

    q_column = list(map(lambda x: extract_phrase(x, q_a_operator_order_dict, list_of_bs_p_tags), q_n_p_tag_tuple_structured_order))
    a_column = list(map(lambda x: extract_phrase(x, q_a_operator_order_dict, list_of_bs_p_tags), a_n_p_tag_tuple_structured_order))

    analysts_name_comp = list(map(lambda x: extract_tagged_names(x, list_of_bs_p_tags), q_n_p_tag_tuple_structured_order))
    executives_name_comp = list(map(lambda x: extract_tagged_names(x, list_of_bs_p_tags), a_n_p_tag_tuple_structured_order))

    analyst_name_column, analysts_company_column = list(map(list, zip(*analysts_name_comp)))
    executive_name_column, executive_position_column = list(map(list, zip(*executives_name_comp)))

    return analyst_name_column, analysts_company_column, executive_name_column, executive_position_column, \
           q_column, a_column, q_n_p_tag_tuple_structured_order_column, a_n_p_tag_tuple_structured_order_column




def one_text_parser_tagged(str_text: str):

    bstext = BeautifulSoup(str_text, 'html.parser')
    list_of_bs_p_tags = bstext('p')

    company_name, company_name_tag_a_info, company_ticker = header_a_tag_company_name(bstext)
    company_name_regex = None
    company_name_desc = head_comp(bstext)
    date_mod, date_pub, date_desc = head_date(bstext)

    q_a_operator_order_dict = get_q_a_operator_order_dict(bstext, list_of_bs_p_tags)

    analyst_name_column, analysts_company_column, \
    executive_name_column, executive_position_column, \
    q_column, a_column, \
    q_n_p_tag_tuple_structured_order_column, \
    a_n_p_tag_tuple_structured_order_column = extract_dialog_info_with_eao_dict(q_a_operator_order_dict, list_of_bs_p_tags)

    result_df_len = len(q_column)

    company_name_column = [company_name] * result_df_len
    company_name_tag_a_info_column = [company_name_tag_a_info] * result_df_len
    company_ticker_column = [company_ticker] * result_df_len
    company_name_regex_column = [company_name_regex] * result_df_len
    company_name_desc_column = [company_name_desc] * result_df_len
    date_mod_column = [date_mod] * result_df_len
    date_pub_column = [date_pub] * result_df_len
    date_desc_column = [date_desc] * result_df_len
    analysts_list_column = [None] * result_df_len
    executives_list_column = [None] * result_df_len
    sys_info_column = [None] * result_df_len

    result_df_column_based = [
        company_name_column, company_name_tag_a_info_column, company_ticker_column,
        company_name_regex_column, company_name_desc_column,
        date_pub_column, date_mod_column, date_desc_column,
        analyst_name_column, analysts_company_column,
        executive_name_column, executive_position_column,
        q_column, a_column,
        q_n_p_tag_tuple_structured_order_column, a_n_p_tag_tuple_structured_order_column,
        analysts_list_column, executives_list_column, sys_info_column
    ]
    result_df = pd.DataFrame(result_df_column_based, index=RESULT_DF_COLUMNS_NAMES).T
    return result_df





if __name__=="__main__":

    file_path = '../data/txt_data/outer/1-526/731_num_11.txt'

    _str_text = read_txt_file_with_decoding(file_path)

    import time
    start = time.time()

    df = one_text_parser_tagged(_str_text)

    end = time.time()
    print(end - start)

    # df.to_excel("test.xlsx")

    bstext = BeautifulSoup(_str_text, 'html.parser')
    list_of_bs_p_tags = bstext('p')


    print()
























