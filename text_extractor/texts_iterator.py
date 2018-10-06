import pandas as pd
import os
import logging
import traceback
import sys
from bs4 import BeautifulSoup
import re

from text_parser.main_parser import main_text_parser
from text_extractor.extractor_file_system_interaction import collect_txts_fs
from text_parser.utils import read_txt_file_with_decoding
from utils import write_error_to_log

TEXT_ITERATOR_CWD = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler_file = os.path.normpath(os.path.join(TEXT_ITERATOR_CWD, '../log/log_text_iterator.log'))
handler = logging.FileHandler(handler_file, encoding="utf-8")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



# def write_error_to_log(logger, **kwargs):
#     logger.error('ERROR_CLASS: {}'.format(sys.exc_info()[0]))
#     logger.error('ERROR_MESSAGE: {}'.format(sys.exc_info()[1]))
#     logger.error('TRACEBACK: {}'.format(traceback.format_exc()))
#     for name, value in kwargs.items():
#         logger.error(name.upper() + ": {}".format(value))



def df_postproc(df, new_columns_dict):
    df_processed = df.copy()
    len_df = len(df_processed)
    for key, value in new_columns_dict.items():
        df_processed[key] = [value] * len_df
    return df_processed



def structurate_data(type):

    XL_SAVE_FOLDER = "../data/xl_results/"
    df_list = []

    if type=="fs":
        if not os.path.exists(XL_SAVE_FOLDER):
            os.mkdir(XL_SAVE_FOLDER)
    elif type == "bd":
        pass
    else:
        raise ValueError("The type should be fs (file system) or db (data base)")


    text_id=0
    iteration_count=0
    for file_path, str_text in collect_txts_fs():
        iteration_count+=1

        try:

            df = main_text_parser(str_text)
            df = df_postproc(
                df,
                {"SYS_INFO_OUTSIDE_PARSER": file_path,
                 "TEXT_ID": text_id}
            )
            text_id+=1
            if type == "fs": df_list.append(df)

        except:
            write_error_to_log(logger=logger, file_path_info=file_path)

        print(iteration_count, text_id)

        if type == "fs":
            if iteration_count%300==0:
                pd.concat(df_list).to_excel(
                    os.path.join(XL_SAVE_FOLDER, 'table{}.xlsx'.format(iteration_count))
                )
                df_list = []
        elif type=="bd":
            pass




if __name__=="__main__":

    # structurate_data("fs")

    from text_parser.head_info_parser import get_analysts_executives_list

    # i = 0
    # for file_path, str_text in collect_txts_fs():
    #     i+=1
    #
    #     bstext = BeautifulSoup(str_text, 'html.parser')
    #
    #     try:
    #         l = get_analysts_executives_list(bstext)
    #         print(l)
    #     except:
    #         print()
    #         print(i, file_path, "EROR - EROR - EROR - EROR - EROR - EROR - EROR - EROR - EROR - EROR - EROR - EROR - EROR")
    #         print()
    #         logger.error(file_path)

    # file_path, str_text = next(collect_txts_fs())
    #
    # file_path = '../data/txt_data/inner/3245_num_12.txt'
    # str_text = read_txt_file_with_decoding(file_path)
    #
    # df = main_text_parser(str_text)
    # df = df_postproc(df, {"SYS_INFO_OUTSIDE_PARSER": file_path, "TEXT_ID": 0})
    #
    # print()












