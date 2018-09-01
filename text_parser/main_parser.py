from bs4 import BeautifulSoup
import pandas as pd

from text_parser.sa_text_parser_untagged_dialog_chunk_approach import one_text_parser_untagged_chunk
from text_parser.sa_text_parser_tagged_dialog import one_text_parser_tagged, is_tagged
from text_parser.utils import file_is_not_full, RESULT_DF_COLUMNS_NAMES



def main_text_parser(str_text):

    bstext = BeautifulSoup(str_text, 'html.parser')

    if file_is_not_full(bstext):

        result_df_from_text = pd.DataFrame(columns=RESULT_DF_COLUMNS_NAMES)

    else:

        if is_tagged(bstext):
            result_df_from_text = one_text_parser_tagged(str_text)
        else:
            result_df_from_text = one_text_parser_untagged_chunk(str_text)

    return result_df_from_text
















