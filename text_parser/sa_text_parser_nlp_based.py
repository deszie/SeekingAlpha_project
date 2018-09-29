import os
from bs4 import BeautifulSoup

from text_parser.utils import read_txt_file_with_decoding, get_text_from_bs_tag, \
    get_list_items_by_index, count_strings_words_intersection, count_words_from_list_in_string, RESULT_DF_COLUMNS_NAMES
from text_parser.head_info_parser import *
from nlp_core.tag_names_extractor import qa_start_find, get_n_strong_tags, expand_analysts_executives_list
from nlp_core.names_extractor import get_names_from_str_tags_list, calc_n_names
from nlp_core.words_lists import FLAG_EXECUTIVE_NAME_WORDS, FLAG_ANALYST_NAME_WORDS
from text_parser.sa_text_parser_tagged_dialog import extract_dialog_info_with_eao_dict



def is_analyst_or_executive_extracted_list_based(tag_text, analyst_executive_list):
    executives = analyst_executive_list["executives"]
    analysts = analyst_executive_list["analysts"]
    intersection_count_executives = list(map(lambda x: count_strings_words_intersection(x, tag_text), executives))
    intersection_count_analysts = list(map(lambda x: count_strings_words_intersection(x, tag_text), analysts))

    max_executive_intersection = max(intersection_count_executives)
    max_analyst_intersection = max(intersection_count_analysts)

    if max_executive_intersection>max_analyst_intersection:
        return "e"
    elif max_executive_intersection<max_analyst_intersection:
        return "a"
    return None



def is_analyst_or_executive_stop_words_based(zip_ae_list_element):
    if zip_ae_list_element[2]=="e":
        return "e"
    elif zip_ae_list_element[2]=="a":
        return "a"
    executive_words_count = count_words_from_list_in_string(zip_ae_list_element[1].lower(), FLAG_EXECUTIVE_NAME_WORDS)
    if executive_words_count>0:
        return "e"
    analyst_words_count = count_words_from_list_in_string(zip_ae_list_element[1].lower(), FLAG_ANALYST_NAME_WORDS)
    if analyst_words_count>0:
        return "a"
    return None


def is_analyst_or_executive_none_collacation_based(zip_ae):
    zip_ae_list = list(zip_ae)
    ae_flag_list = list(map(lambda x: x[2], zip_ae_list))
    l = len(ae_flag_list)
    for i in range(1,l-1):
        cur_ = ae_flag_list[i]
        prev_ = ae_flag_list[i - 1]
        next_ = ae_flag_list[i + 1]
        if (cur_ is None) & ("Operator" not in zip_ae_list[i][1]):
            if (prev_=="a") & (next_=="a"):
                ae_flag_list[i] = "e"
            elif (prev_=="e") & (next_=="e"):
                ae_flag_list[i] = "a"
    return ae_flag_list



def _correct_ae_flags(ae_marks, strong_tags_after_qa_list, strong_tags_text):
    zip_ae_list = zip(strong_tags_after_qa_list[:-1], strong_tags_text[:-1], ae_marks[:-1])
    zip_ae_list_stop_words_correction = list(map(is_analyst_or_executive_stop_words_based, zip_ae_list))
    zip_ae_list_corrected_1 = zip(strong_tags_after_qa_list[:-1], strong_tags_text[:-1],
                                  zip_ae_list_stop_words_correction)
    ae_list = is_analyst_or_executive_none_collacation_based(zip_ae_list_corrected_1)
    zip_ae_list_corrected = list(zip(strong_tags_after_qa_list[:-1], ae_list))
    return zip_ae_list_corrected


def separate_analysts_executives(zip_ae_list):
    n_exetuves_tags = list(map(lambda x: x[0], filter(lambda x: x[1]=="e", zip_ae_list)))
    n_analysts_tags = list(map(lambda x: x[0], filter(lambda x: x[1]=="a", zip_ae_list)))
    return n_exetuves_tags, n_analysts_tags


def get_n_operator_flags(strong_tags_text):
    return list(map(lambda x: x[0], filter(lambda x: x[1]=="Operator", enumerate(strong_tags_text))))

def get_n_copyright_policy_flag(strong_tags_text):
    return list(map(lambda x: x[0], filter(lambda x: "copyright policy:" in x[1].lower(), enumerate(strong_tags_text))))




def one_text_parser_nlp_based(str_text: str):
    bstext = BeautifulSoup(str_text, 'html.parser')
    list_of_bs_p_tags = bstext('p')

    company_name, company_name_tag_a_info, company_ticker = header_a_tag_company_name(bstext)
    company_name_regex = None
    company_name_desc = head_comp(bstext)
    date_mod, date_pub, date_desc = head_date(bstext)

    list_of_p_tags_text = list(map(get_text_from_bs_tag, list_of_bs_p_tags))

    names_list = get_all_mentioned_names(list_of_p_tags_text)

    analysts_executives_list = get_analysts_executives_list(bstext, names_list)
    analysts_executives_list = expand_analysts_executives_list(analysts_executives_list)

    qa_start = qa_start_find(list_of_bs_p_tags)
    n_strong_tags = get_n_strong_tags(list_of_bs_p_tags)
    strong_tags_after_qa_list = list(filter(lambda x: x>qa_start, n_strong_tags))

    strong_tags_text = get_list_items_by_index(list_of_p_tags_text, strong_tags_after_qa_list)
    ae_marks = list(map(lambda x: is_analyst_or_executive_extracted_list_based(x, analysts_executives_list), strong_tags_text))

    zip_ae_list_corrected = _correct_ae_flags(ae_marks, strong_tags_after_qa_list, strong_tags_text)

    n_exetuves_tags, n_analysts_tags = separate_analysts_executives(zip_ae_list_corrected)
    strong_tags_other_than_ea = list(set(strong_tags_after_qa_list) - set.union(set(n_exetuves_tags), set(n_analysts_tags)))

    eao_dict_for_dialog_info_extraction = {
        'operator_order_list': sorted(strong_tags_other_than_ea),
        'questions_order_list': sorted(n_analysts_tags),
        'answers_order_list': sorted(n_exetuves_tags)
    }
    analyst_name_column, analysts_company_column, \
    executive_name_column, executive_position_column, \
    q_column, a_column, \
    q_n_p_tag_tuple_structured_order_column, \
    a_n_p_tag_tuple_structured_order_column = extract_dialog_info_with_eao_dict(eao_dict_for_dialog_info_extraction, list_of_bs_p_tags)

    result_df_len = len(q_column)

    n_operator_strong_tags = get_n_operator_flags(list_of_p_tags_text)
    n_operator_strong_tags_after_qa_start = list(filter(lambda x: x > qa_start, n_operator_strong_tags))
    copyright_policy_flag = get_n_copyright_policy_flag(list_of_p_tags_text)
    operator_copyright_strong_tags = n_operator_strong_tags_after_qa_start + copyright_policy_flag
    n_unidentified_strong_tags = len(set(strong_tags_other_than_ea) - set(operator_copyright_strong_tags))

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
    sys_info_column = ["n_unidentified_strong_tags = {}".format(n_unidentified_strong_tags)] * result_df_len

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

    file_path = '../data/txt_data/inner/3174_num_7.txt'
    file_path = '../data/txt_data/inner/3193_num_12.txt'
    file_path = '../data/txt_data/inner/3233_num_3.txt'

    _str_text = read_txt_file_with_decoding(file_path)

    import time
    start = time.time()

    df = one_text_parser_nlp_based(_str_text)

    end = time.time()
    print(end - start)

    df.to_excel("test.xlsx")

    print()


































