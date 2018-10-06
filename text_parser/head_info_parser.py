import pandas as pd
from bs4 import BeautifulSoup
import re

from text_parser.utils import read_txt_file_with_decoding, get_text_from_bs_tag, \
    get_list_items_by_index, get_numbers_between_interval, count_emerging_words, \
    count_words_from_list_in_string
from nlp_core.names_extractor import *


def name_company_split(name):
    undef_list = ['Unidentified Company Representative',
                  'Unidentified Corporate Participant',
                  'Unidentified Analyst',
                  'Unknown Attendee',
                  'Unknown Executive']
    undef_in = False
    for undef_id in undef_list:
        if undef_id in name:
            result_list = [undef_id, 'Unidentified Company']
            undef_in = True
            break
    if not undef_in:
        utf_name = name.encode('utf-8')
        result_list = [name, 'No_company_found']
        if b'\xe2\x80\x93' in utf_name:
            result_list = utf_name.split(b'\xe2\x80\x93')
            result_list = [result_list[0].decode(), result_list[1].decode()]
        elif '-' in name:
            result_list = name.split('-')
        result_list = [result_list[0], ' - '.join(result_list[1:])]
    return list(map(lambda x: x.strip(), result_list))



def date_getter(s):
    res = s.replace('Call End', '')
    res = res.replace('Call Start', '')
    first = r'[A-Z][a-z]+\,?\ +\d+\,? \d+\,?\;?\ +\d+?.?\d+.+'
    second = r'[A-Z][a-z]+\,?\ +\d+\,?\ +\d+\ +-\ +\d+?.?\d+.+'
    third = r'[A-Z][a-z]+\,?\ +\d+\,?\ +\d+\ +at\ +\d+?.?\d+.+'
    forth = r'[A-Z][a-z]+\,?\ +\d+\,? \d+'
    if len(re.findall(first, res))!=0:
        ret = re.findall(first, res)
    elif len(re.findall(second, res))!=0:
        ret = re.findall(second, res)
    elif len(re.findall(third, res))!=0:
        ret = re.findall(third, res)
    elif len(re.findall(forth, res)) != 0:
        ret = re.findall(forth, res)
    else:
        ret = res
    return ret[0].split('+')[0]



def head_date(bstext):
    time_tags = bstext('time')
    head_time_list = [time_tags[0].get('datetime'),
                      time_tags[1].get('content'),
                      time_tags[1].text]
    return head_time_list



def comp_getter(s):
    res = s.replace('Call End', '')
    res = res.replace('Call Start', '')
    try:
        pat = re.findall(r'.+\([A-Z]+.+\)', res)[0]
        if '+' in pat:
            parts = pat.split('+')
            if 'Inc' in parts[0]:
                pat = re.findall(r'.+Inc{?}*', parts[0])[0]
            else:
                for p in parts:
                    search_c = re.search(r'\(.+[A-Z]+\)', p)
                    if search_c is not None:
                        search_c = search_c.group()
                    else:
                        search_c = ""
                    if len(search_c)!=0:
                        pat = p
    except:
        if '+' in res:
            parts = res.split('+')
            if 'Inc' in parts[0]:
                pat = re.findall(r'.+Inc{?}*', parts[0])[0]
            else:
                for p in parts:
                    search_c = re.search(r'\(.+[A-Z]+\)', p)
                    if search_c is not None:
                        search_c = search_c.group()
                    else:
                        search_c = ""
                    if len(search_c)!=0:
                        pat = p
    return pat



def head_comp(bstext):
    div_ahd_list = bstext('div', id="a-hd")
    if len(div_ahd_list)>0:
        div_ahd = div_ahd_list[0]
    h1_tag_list = div_ahd('h1')
    if len(h1_tag_list)>0:
        return h1_tag_list[0].text
    else:
        return None



def all_inf_date_comp(bstext, header):
    inf_list = []
    # comp_above, comp_head
    # date_above, date_mod, date_pub, date_pub_content
    # company part
    try:
        inf_list.append(comp_getter(header))
    except:
        inf_list.append('ERROR')
    inf_list.append(head_comp(bstext))
    # date part
    try:
        inf_list.append(date_getter(header))
    except:
        inf_list.append('ERROR')
    inf_list = inf_list + head_date(bstext)
    return inf_list




def header_a_tag_company_name(bstext):
    header_tag = bstext.find_all("header")[0]
    a_tag_list = header_tag.find_all("a")
    a_tag = None
    for a in a_tag_list:
        if "/symbol/" in a.get('href'):
            a_tag = a
    company_name = a_tag.text
    company_name_tag_a_info = a_tag.get('title')
    company_ticker = a_tag.get('href').replace("/symbol/", "")
    return company_name, company_name_tag_a_info, company_ticker



def calc_prct_change(number_list):
    prct_change_list = [None]
    zip_list = list(zip(number_list, number_list[1:]))
    l = len(zip_list)
    for i in range(l):
        n1, n2 = zip_list[i]
        if n1==0:
            prev_n1, prev_n2 = zip_list[i-1]
            prct_change_list.append((n2 + 1) / (prev_n1 + 1))
        else:
            prct_change_list.append((n2+1)/(n1+1))
    # return [None] + [(n2+1)/(n1+1) for n1, n2 in zip(number_list, number_list[1:])]
    return prct_change_list

def get_first_large_change(prct_chng_list, threshold=30):
    large_chngs = [None] + list(map(lambda x: 1 if x>=threshold else 0, prct_chng_list[1:]))
    for i in range(len(large_chngs)):
        if large_chngs[i]==1:
            return i
    return None







def get_abrupt_start_n(list_p_tags_text):
    abrupt_start_n = None
    for p in range(len(list_p_tags_text)):
        if "[Abrupt Start]" in list_p_tags_text[p]:
            abrupt_start_n = p
            break
    return abrupt_start_n


def _get_aeo_list_headers(p_tags_str):
    executives_flag = None
    analysts_flag_plural = None
    analyst_flag_singular = None
    operator_flag = None
    # str_tags = list(map(str, p1_tags))
    for t in range(len(p_tags_str)):
        if "<strong>Executives</strong>" in p_tags_str[t]:
            executives_flag = t
        if "<strong>Analysts</strong>" in p_tags_str[t]:
            analysts_flag_plural = t
        if "<strong>Analyst</strong>" in p_tags_str[t]:
            analyst_flag_singular = t
        if "<strong>Operator</strong>" in p_tags_str[t]:
            operator_flag = t
    analysts_flag = analysts_flag_plural
    if analysts_flag_plural is None:
        analysts_flag = analyst_flag_singular
    return executives_flag, analysts_flag, operator_flag



def _get_n_tags_with_names(p1_tags_text, names_list):
    n_names_tags = enumerate(map(lambda x: count_emerging_words(x, names_list), p1_tags_text))
    n_tags_with_names = list(filter(lambda x: x[1]>0, n_names_tags))
    n_tags, count_names = list(zip(*n_tags_with_names))
    return n_tags, count_names




def _if_eao(p1_tags_text_list, executives_flag, analysts_flag, operator_flag, first_large_change, n_tags_with_name):
    analysts_list_end = first_large_change

    executive_indexs = get_numbers_between_interval(n_tags_with_name, executives_flag + 1, analysts_flag)
    executive_list = get_list_items_by_index(p1_tags_text_list, executive_indexs)

    if operator_flag<first_large_change:
        analyst_indexs = get_numbers_between_interval(n_tags_with_name, analysts_flag + 1, operator_flag)
        analyst_list = get_list_items_by_index(p1_tags_text_list, analyst_indexs)
    else:
        analyst_indexs = get_numbers_between_interval(n_tags_with_name, analysts_flag + 1, analysts_list_end)
        analyst_list = get_list_items_by_index(p1_tags_text_list, analyst_indexs)
    return {"executives": executive_list, "analysts": analyst_list}



def _if_ea(p1_tags_text_list, executives_flag, analysts_flag, operator_flag, first_large_change, n_tags_with_name):
    analysts_list_end = first_large_change

    executive_indexs = get_numbers_between_interval(n_tags_with_name, executives_flag + 1, analysts_flag)
    executive_list = get_list_items_by_index(p1_tags_text_list, executive_indexs)

    analyst_indexs = get_numbers_between_interval(n_tags_with_name, analysts_flag + 1, analysts_list_end)
    analyst_list = get_list_items_by_index(p1_tags_text_list, analyst_indexs)

    return {"executives": executive_list, "analysts": analyst_list}



def _if_eo(p1_tags_text_list, executives_flag, analysts_flag, operator_flag, first_large_change, n_tags_with_name):
    executives_list_end = first_large_change

    if operator_flag<executives_list_end:
        executive_indexs = get_numbers_between_interval(n_tags_with_name, executives_flag + 1, operator_flag)
        executive_list = get_list_items_by_index(p1_tags_text_list, executive_indexs)
    else:
        executive_indexs = get_numbers_between_interval(n_tags_with_name, executives_flag + 1, executives_list_end)
        executive_list = get_list_items_by_index(p1_tags_text_list, executive_indexs)

    return {"executives": executive_list, "analysts": []}



def _if_e(p1_tags_text_list, executives_flag, analysts_flag, operator_flag, first_large_change, n_tags_with_name):
    executives_list_end = first_large_change

    executive_indexs = get_numbers_between_interval(n_tags_with_name, executives_flag + 1, executives_list_end)
    executive_list = get_list_items_by_index(p1_tags_text_list, executive_indexs)

    return {"executives": executive_list, "analysts": []}



def get_analysts_executives_list(bstext, text_names_list):
    p1_tags = bstext.find_all("p", attrs={"class": "p p1"})
    p1_tags_text_list = list(map(get_text_from_bs_tag, p1_tags))
    p1_tags_str_list = list(map(str, p1_tags))

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

    if executives_flag>first_large_change_flag:
        raise ValueError("executives_flag > first_large_change")
    if (analysts_flag is not None) and (analysts_flag>first_large_change_flag):
        raise ValueError("analysts_flag > first_large_change")

    n_tags_with_name, count_names_in_tags = _get_n_tags_with_names(p1_tags_text_before_main_flags_list, text_names_list)

    # names = get_names_from_str_tags_list(p1_tags_text_before_main_flags_list)
    # n_names = calc_n_names(names)
    # n_tags_with_name_ = get_n_one_name_tags(n_names)

    print()

    if executives_flag is None:
        raise ValueError("There are no executives header")

    if (analysts_flag is not None) & (operator_flag is not None):
        return _if_eao(p1_tags_text_before_main_flags_list,
                       executives_flag,
                       analysts_flag,
                       operator_flag,
                       first_large_change_flag,
                       n_tags_with_name)

    elif (analysts_flag is not None) & (operator_flag is None):
        return _if_ea(p1_tags_text_before_main_flags_list,
                       executives_flag,
                       analysts_flag,
                       operator_flag,
                       first_large_change_flag,
                       n_tags_with_name)

    elif (analysts_flag is None) & (operator_flag is not None):
        return _if_eo(p1_tags_text_before_main_flags_list,
                       executives_flag,
                       analysts_flag,
                       operator_flag,
                       first_large_change_flag,
                       n_tags_with_name)

    elif (analysts_flag is None) & (operator_flag is None):
        return _if_e(p1_tags_text_before_main_flags_list,
                       executives_flag,
                       analysts_flag,
                       operator_flag,
                       first_large_change_flag,
                       n_tags_with_name)

    else:
        raise ValueError("Troubles with Analysts and Operator flags")



















if __name__=="__main__":

    from nlp_core.names_extractor import get_all_mentioned_names

    file_path = "../data/txt_data/inner/3250_num_18.txt"
    # file_path = "../data/txt_data/inner/3073_num_19.txt"
    # file_path = "../data/txt_data/inner/3266_num_28.txt"
    # file_path = "../data/txt_data/inner/3000_num_5.txt"

    _str_text = read_txt_file_with_decoding(file_path)
    bstext = BeautifulSoup(_str_text, 'html.parser')
    list_of_bs_p_tags = bstext('p')
    p_tags_text_list = list(map(get_text_from_bs_tag, list_of_bs_p_tags))
    names_list = get_all_mentioned_names(p_tags_text_list)
    t = get_analysts_executives_list(bstext, names_list)
    t
    bstext("p")[:20]

    print()






