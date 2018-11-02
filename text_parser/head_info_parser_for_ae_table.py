import os
import pandas as pd
import re

from text_parser.utils import get_text_from_bs_tag, get_list_items_by_index, \
    get_numbers_between_interval, drop_short_strings
from text_parser.head_info_parser_for_untagged import find_first_tag_with_stop_words, \
    get_abrupt_start_n, _get_aeo_list_headers, calc_prct_change, get_first_large_change, \
    _get_n_tags_with_names


def get_qa_names(q_a_operator_order_dict, list_of_bs_p_tags):
    q_list = q_a_operator_order_dict["questions_order_list"]
    a_list = q_a_operator_order_dict["answers_order_list"]
    bs_p_tags_text = list(map(get_text_from_bs_tag, list_of_bs_p_tags))

    executives_list_repeated = get_list_items_by_index(bs_p_tags_text, a_list)
    analysts_list_repeated = get_list_items_by_index(bs_p_tags_text, q_list)

    executives_list = list(set(executives_list_repeated))
    analysts_list = list(set(analysts_list_repeated))

    return executives_list, analysts_list







def _if_eao(p1_tags_text_list,
            executives_flag,
            analysts_flag,
            operator_flag,
            first_large_change):

    n_tags_executives_potential_names = list(range(len(p1_tags_text_list)))
    n_tags_analysts_potential_names = list(range(len(p1_tags_text_list)))

    executive_indexs = get_numbers_between_interval(n_tags_executives_potential_names, executives_flag + 1, analysts_flag)
    executive_list = get_list_items_by_index(p1_tags_text_list, executive_indexs)
    executive_list = drop_short_strings(executive_list)

    if operator_flag<first_large_change:
        analysts_list_end = operator_flag
    else:
        analysts_list_end = first_large_change

    analyst_indexs = get_numbers_between_interval(n_tags_analysts_potential_names, analysts_flag + 1, analysts_list_end)
    analyst_list = get_list_items_by_index(p1_tags_text_list, analyst_indexs)
    analyst_list = drop_short_strings(analyst_list)

    return {"executives": executive_list, "analysts": analyst_list}



def _if_ea(p1_tags_text_list,
           executives_flag,
           analysts_flag,
           operator_flag,
           first_large_change):

    n_tags_executives_potential_names = list(range(len(p1_tags_text_list)))
    n_tags_analysts_potential_names = list(range(len(p1_tags_text_list)))
    analysts_list_end = first_large_change

    executive_indexs = get_numbers_between_interval(n_tags_executives_potential_names, executives_flag + 1, analysts_flag)
    executive_list = get_list_items_by_index(p1_tags_text_list, executive_indexs)

    analyst_indexs = get_numbers_between_interval(n_tags_analysts_potential_names, analysts_flag + 1, analysts_list_end)
    analyst_list = get_list_items_by_index(p1_tags_text_list, analyst_indexs)

    return {"executives": executive_list, "analysts": analyst_list}



def _if_eo(p1_tags_text_list,
           executives_flag,
           analysts_flag,
           operator_flag,
           first_large_change):

    n_tags_executives_potential_names = list(range(len(p1_tags_text_list)))
    # n_tags_analysts_potential_names = list(range(len(p1_tags_text_list)))

    if operator_flag<first_large_change:
        executives_list_end = operator_flag
    else:
        executives_list_end = first_large_change

    executive_indexs = get_numbers_between_interval(n_tags_executives_potential_names, executives_flag + 1, executives_list_end)
    executive_list = get_list_items_by_index(p1_tags_text_list, executive_indexs)

    return {"executives": executive_list, "analysts": []}



def _if_e(p1_tags_text_list,
          executives_flag,
          analysts_flag,
          operator_flag,
          first_large_change):

    n_tags_executives_potential_names = list(range(len(p1_tags_text_list)))
    # n_tags_analysts_potential_names = list(range(len(p1_tags_text_list)))

    executives_list_end = first_large_change

    executive_indexs = get_numbers_between_interval(n_tags_executives_potential_names, executives_flag + 1, executives_list_end)
    executive_list = get_list_items_by_index(p1_tags_text_list, executive_indexs)

    return {"executives": executive_list, "analysts": []}





def get_ae_dict_rules_based(bstext, q_a_operator_order_dict=None, list_of_bs_p_tags=None):
    p1_tags = bstext.find_all("p", attrs={"class": "p p1"})
    p1_tags_text_list = list(map(get_text_from_bs_tag, p1_tags))
    p1_tags_str_list = list(map(str, p1_tags))

    if len(p1_tags)<3:
        re_p1 = re.compile(r'.+ p p1$')
        p1_tags = bstext.find_all("p", attrs={"class": re_p1})
        p1_tags_text_list = list(map(get_text_from_bs_tag, p1_tags))
        p1_tags_str_list = list(map(str, p1_tags))

    # executives_participated_list, analysts_participated_list = get_qa_names(q_a_operator_order_dict, list_of_bs_p_tags)
    # n_executive_potential_names, count_e_names_in_tags = _get_n_tags_with_names(p1_tags_text_list, executives_participated_list)
    # n_analysts_potential_names, count_a_names_in_tags = _get_n_tags_with_names(p1_tags_text_list, analysts_participated_list)


    abrupt_start_flag = get_abrupt_start_n(p1_tags_text_list)
    stop_word_tag_flag = find_first_tag_with_stop_words(p1_tags_text_list) - 1

    executives_flag, analysts_flag, operator_flag = _get_aeo_list_headers(p1_tags_str_list)

    if abrupt_start_flag is not None:
        p1_tags_text_before_main_flags_list = p1_tags_text_list[:abrupt_start_flag]
    else:
        p1_tags_text_before_main_flags_list = p1_tags_text_list[:stop_word_tag_flag]

    p1_tags_len_list = list(map(len, p1_tags_text_before_main_flags_list))
    prct_chng_list = calc_prct_change(p1_tags_len_list)
    first_large_change = get_first_large_change(prct_chng_list, threshold=30)

    first_large_change_flag = len(p1_tags_text_before_main_flags_list)
    if first_large_change is not None:
        first_large_change_flag = first_large_change-1

    if executives_flag is None:
        raise ValueError("There are no executives header")

    if (analysts_flag is not None) & (operator_flag is not None):
        return _if_eao(p1_tags_text_before_main_flags_list,
                       executives_flag,
                       analysts_flag,
                       operator_flag,
                       first_large_change_flag)

    elif (analysts_flag is not None) & (operator_flag is None):
        return _if_ea(p1_tags_text_before_main_flags_list,
                       executives_flag,
                       analysts_flag,
                       operator_flag,
                       first_large_change_flag)

    elif (analysts_flag is None) & (operator_flag is not None):
        return _if_eo(p1_tags_text_before_main_flags_list,
                       executives_flag,
                       analysts_flag,
                       operator_flag,
                       first_large_change_flag)

    elif (analysts_flag is None) & (operator_flag is None):
        return _if_e(p1_tags_text_before_main_flags_list,
                       executives_flag,
                       analysts_flag,
                       operator_flag,
                       first_large_change_flag)

    else:
        raise ValueError("Troubles with Analysts and Operator flags")











