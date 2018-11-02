import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np

from text_parser.utils import *
from text_parser.sa_chunks_parser import *
from text_parser.head_info_parser_for_untagged import *



def get_executives_names_from_html_structure(list_of_bs_p_tags, executives_flag, analysts_flag):
    executives_name = []
    executives_pos = []
    for i in range(executives_flag + 1, analysts_flag):
        ex_text = list_of_bs_p_tags[i].text
        if len(ex_text)>0:
            executives_name.append(name_company_split(ex_text)[0])
            executives_pos.append(name_company_split(ex_text)[1])
    executives_name = list(map(lambda x: x.strip(), executives_name))
    executives_pos = list(map(lambda x: x.strip(), executives_pos))
    exec_dict = dict(
        zip(
            executives_name,
            executives_pos
        )
    )
    return exec_dict

def get_analysts_names_from_html_structure(list_of_bs_p_tags, analysts_flag, stop_flag):
    analysts = []
    for i in range(analysts_flag+1, stop_flag):
        a_text = list_of_bs_p_tags[i].text
        if len(a_text)>0:
            cur_analyst = name_company_split(a_text)
            cur_analyst = list(map(lambda x: x.strip(), cur_analyst))
            analysts.append(cur_analyst)
    analysts_dict = dict(analysts)
    return analysts_dict



def get_head_info(list_of_bs_p_tags, bstext):
    e_flag, a_flag, stop_flag = get_names_list_chunks(list_of_bs_p_tags)

    header = '+'.join([(lambda x: x.text)(t) for t in list_of_bs_p_tags[:e_flag]])
    comp_date_inf = all_inf_date_comp(bstext, header)

    exec_dict = get_executives_names_from_html_structure(list_of_bs_p_tags, e_flag, a_flag)
    analysts_dict = get_analysts_names_from_html_structure(list_of_bs_p_tags, a_flag, stop_flag)

    return comp_date_inf, exec_dict, analysts_dict


def get_oper_chunks(list_of_bs_p_tags, qa_start):
    oper_flags = []
    for p in range(qa_start, len(list_of_bs_p_tags)):
        if '<strong>Operator' in str(list_of_bs_p_tags[p]):
            oper_flags.append(
                p
            )
    oper_chunks =  []
    for f in range(len(oper_flags) - 1):
        oper_chunks.append(
            list_of_bs_p_tags[oper_flags[f]:oper_flags[f + 1]]
        )
    return oper_chunks



def get_qa_chunks(oper_chunk, analysts_dict):
    q_blocks = []
    respective_analysts = []
    for p in range(len(oper_chunk)):
        # if p_data[p].text in analysts:

        # print(oper_chunk[p].text)
        # print(check_list_strings_in_strings(oper_chunk[p].text, list(analysts_dict.keys())))
        # print('--------------------------------------')
        #
        # if check_string_in_list_strings(oper_chunk[p].text.replace(' ', ''),
        #                                 list(map(lambda x: x.replace(' ', ''), analysts_dict.keys()))):

        if check_list_strings_in_string(oper_chunk[p].text, list(analysts_dict.keys())):
            q_blocks.append(p)

            respective_analysts_name_list = pd.unique(list(filter(lambda x: x in oper_chunk[p].text, list(analysts_dict.keys()))))
            if len(respective_analysts_name_list)==1:
                respective_analyst_name = respective_analysts_name_list[0]
            else:
                raise ValueError("get_qa_chunks, respective_analysts issue")

            respective_analysts.append(respective_analyst_name)

    qa_chunks = []
    for i in range(len(q_blocks) - 1):
        qa_chunks.append(
            oper_chunk[q_blocks[i]:q_blocks[i + 1]]
        )
    return qa_chunks, respective_analysts



def get_qa_pairs(qa_chunk, exec_dict):

    qa_pairs = []

    q = []
    for j in range(1, len(qa_chunk)):
        if qa_chunk[j].text.replace(' ', '') in [e.replace(' ', '') for e in exec_dict.keys()]:
            break
        q.append(qa_chunk[j].text)

    respective_executives = []
    answers_ids = []
    for j in range(1, len(qa_chunk)):
        if qa_chunk[j].text.replace(' ', '') in [e.replace(' ', '') for e in exec_dict.keys()]:
            answers_ids.append(j)
            respective_executives.append(qa_chunk[j].text)
    answers_ids.append(len(qa_chunk))

    for a_id in range(len(answers_ids) - 1):
        a = qa_chunk[answers_ids[a_id] + 1:answers_ids[a_id + 1]]
        qa_pairs.append([
            ' '.join(q), ' '.join(list(map(get_text_from_bs_tag, a)))
        ])
    return qa_pairs, respective_executives




def one_text_parser_untagged_chunk(str_text: str):

    result = []

    # result_df_columns = [
    #     'Company_name',
    #     'Company_name_tag_a_info',
    #     'Company_ticker_symbol_tag_a_info',
    #     'Company_name_regex_find',
    #     'Company_name_description',
    #     # 'Date',
    #     'Date_modified',
    #     'Date_published',
    #     'Date_desc',
    #     'Analyst',
    #     'Analyst_bank',
    #     'Executive_Name',
    #     'Executive_position',
    #     'Question',
    #     'Answer',
    #     'Q_n_tag',
    #     'A_n_tag',
    #     # 'Analytics_order',
    #     # 'Analytics_question_order',
    #     # 'Exec_answer_order',
    #     'Analysts_list',
    #     'Executives_list',
    #     # 'File_path'
    #     'SYS_INFO'
    # ]

    # str_text = read_txt_file(file_path)
    bs_text = BeautifulSoup(str_text, 'html.parser')
    list_of_bs_p_tags = bs_text('p')

    skip_iter_flag = file_is_not_full(list_of_bs_p_tags)

    if skip_iter_flag:
        return pd.DataFrame(columns=RESULT_DF_COLUMNS_NAMES)
    else:
        comp_date_inf, exec_dict, analysts_dict = get_head_info(list_of_bs_p_tags, bs_text)

        qa_start = qa_start_find(list_of_bs_p_tags)

        oper_chunks = get_oper_chunks(list_of_bs_p_tags, qa_start)

        analytics_order = 0
        for o in range(len(oper_chunks)):

            oper_chunk = oper_chunks[o]
            qa_chunks, respective_analysts = get_qa_chunks(oper_chunk, analysts_dict)

            # respective_analysts = list(map(lambda x: name_company_split[x][0], respective_analysts))

            analytics_order += 1
            question_order = 0
            for qa in range(len(qa_chunks)):

                qa_chunk = qa_chunks[qa]
                qa_pairs, respective_executives = get_qa_pairs(qa_chunk, exec_dict)

                question_order += 1
                answer_order = 0
                for i_pair in range(len(qa_pairs)):

                    qa_pair = qa_pairs[i_pair]

                    answer_order += 1

                    analytics_name = respective_analysts[qa]
                    analytics_comp = analysts_dict[analytics_name]
                    executive_name = respective_executives[i_pair]
                    executive_comp = exec_dict[executive_name]
                    q = qa_pair[0]
                    a = qa_pair[1]

                    sys_info = "analytics_order={}, question_order={}, answer_order={}".format(
                        analytics_order, question_order, answer_order)

                    result.append([
                        None,               # Company_name
                        None,               # Company_name_tag_a_info
                        None,               # Company_ticker_symbol_tag_a_info
                        comp_date_inf[0],   # Company_name_regex_find
                        comp_date_inf[1],   # Company_name_description
                        # comp_date_inf[2],   # date
                        comp_date_inf[4],  # date pub
                        comp_date_inf[3],   # date mod
                        comp_date_inf[5],   # date pub content
                        analytics_name,     # analytics name
                        analytics_comp,     # analytics company
                        executive_name,     # exec name
                        executive_comp,     # exec company
                        q,                  # question
                        a,                  # answer
                        None,               # Q_n_tag
                        None,               # A_n_tag
                        # analytics_order,    # analytics_order
                        # question_order,     # analytics_q_order
                        # answer_order,       # exec_a_order
                        str(analysts_dict), # dict of analysts
                        str(exec_dict),     # dcit of executives
                        # file_path           # path_to_file
                        sys_info            # SYS_INFO

                    ])

    result_df = pd.DataFrame(result, columns=RESULT_DF_COLUMNS_NAMES)

    return result_df



if __name__=="__main__":


    wd = ''
    file_path = wd + '../data/txt_data/inner/3245_num_12.txt'
    # file_path = wd + '../data/txt_data/outer/3560-4824/3736_num_0.txt'

    _str_text = read_txt_file_with_decoding(file_path)
    bstext = BeautifulSoup(_str_text, 'html.parser')

    result_df = one_text_parser_untagged_chunk(_str_text)





    header_tag_str = str(bstext.find_all("header")[0])
    href_content = re.findall(r'href="/symbol/.+?"', header_tag_str)[0][5:]
    company_name_a_tag = bstext.find_all("a", attrs={"href": href_content.replace('"','')})[0]

    list_of_bs_p_tags = bstext('p')
    qa_start = qa_start_find(list_of_bs_p_tags)
    qa_ses = list_of_bs_p_tags[qa_start:]

    flags = get_names_list_chunks(list_of_bs_p_tags)

    comp_date_inf, exec_dict, analysts_dict = get_head_info(list_of_bs_p_tags, bstext)



    oper_chunks = get_oper_chunks(list_of_bs_p_tags, qa_start)

    print(len(oper_chunks))

    qa_chunks, respective_analysts = get_qa_chunks(oper_chunks[0], analysts_dict)

    print(len(qa_chunks))

    qa_chunk = qa_chunks[2]

    qa_pairs, respective_executives = get_qa_pairs(qa_chunk, exec_dict)



    print()

# wd = ''
# file_path = wd + 'data/inner/3107_num_0.txt'
#
# text_file = open(file_path, "r")
# lines = text_file.read()
# text_file.close()
# text = BeautifulSoup(lines, 'html.parser')
# text_data = text('p')
#
# # df1, df2 = one_text_reader(file_path)
#
# comp_date_inf, exec_dict, analysts_dict = get_head_info(text_data, text)
#
# print("analyst", len(analysts_dict))
# print("exec", len(exec_dict))
#
#
# qa_start = qa_start_find(text_data)
# oper_chunks = get_oper_chunks(text_data, qa_start)
#
# get_qa_chunks(oper_chunks[2], analysts_dict)

# qa_chunks, respective_analysts = get_qa_chunks(oper_chunks[3], analysts_dict)
#
# qa_pairs, respective_executives = get_qa_pairs(qa_chunk, exec_dict)



