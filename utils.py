import os
from bs4 import BeautifulSoup
import logging
import traceback
import pandas as pd
import sys
import collections

from text_extractor.extractor_file_system_interaction import collect_txts_fs
from text_parser.head_info_parser import header_a_tag_company_name, head_date
from text_parser.utils import file_is_not_full, RESULT_DF_COLUMNS_NAMES



UTILS_CWD = os.path.dirname(os.path.realpath(__file__))
XL_TEXT_SAVE_FOLDER = "data/xl_text_main_info/"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler_file = os.path.normpath(os.path.join(UTILS_CWD, 'log/log_utils.log'))
handler = logging.FileHandler(handler_file, encoding="utf-8")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



def write_error_to_log(logger, **kwargs):
    logger.error('ERROR_CLASS: {}'.format(sys.exc_info()[0]))
    logger.error('ERROR_MESSAGE: {}'.format(sys.exc_info()[1]))
    logger.error('TRACEBACK: {}'.format(traceback.format_exc()))
    for name, value in kwargs.items():
        logger.error(name.upper() + ": {}".format(value))


def parse_log_file(file_path):
    pass


def fs_txt_stats_calc():

    if not os.path.exists(XL_TEXT_SAVE_FOLDER):
        os.mkdir(XL_TEXT_SAVE_FOLDER)

    df_list = []

    iteration_count=0
    for file_path, str_text in collect_txts_fs():
        iteration_count+=1

        print(iteration_count, file_path)

        try:

            bstext = BeautifulSoup(str_text, 'html.parser')

            company_name, company_name_tag_a_info, company_ticker = header_a_tag_company_name(bstext)
            date_mod, date_pub, date_desc = head_date(bstext)

            if not file_is_not_full(bstext):
                df = pd.DataFrame([[company_name, company_name_tag_a_info, company_ticker, date_pub, date_mod, date_desc]],
                                  columns=["Company_name", "Company_name_tag_a_info", "Company_name_ticker", "Date_pub", "Date_mod", "Date_desc"])
                df_list.append(df)

            if iteration_count%1000==0:
                pd.concat(df_list).to_excel(
                    os.path.join(XL_TEXT_SAVE_FOLDER, 'table{}.xlsx'.format(iteration_count))
                )
                df_list = []

        except:

            write_error_to_log(logger=logger, file_path_info=file_path)


def fs_xl_results_stats_calc(XL_SAVE_FOLDER):
    # XL_SAVE_FOLDER = "data/xl_results/"
    xl_files = os.listdir(XL_SAVE_FOLDER)

    df_list = []
    for file in xl_files:

        print(file)

        df = pd.read_excel(os.path.join(XL_SAVE_FOLDER, file))
        info_df = df[['Company_name', 'Date_pub']].drop_duplicates()
        df_list.append(info_df)

    joint_df = pd.concat(df_list)

    def get_year(x):
        return x.year
    years = pd.to_datetime(joint_df['Date_pub']).apply(get_year)
    counter = collections.Counter(years)
    return pd.DataFrame(list(counter.items()))

if __name__=="__main__":

    # fs_txt_stats_calc()

    # df_xl = fs_xl_results_stats_calc("data/xl_results/")
    # df_xl.to_excel("freq_xl.xlsx")

    df_txt = fs_xl_results_stats_calc("data/xl_text_main_info/")
    df_txt.to_excel("freq_txt.xlsx")































