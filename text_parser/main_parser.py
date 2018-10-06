from bs4 import BeautifulSoup
import pandas as pd

from text_parser.sa_text_parser_untagged_dialog_chunk_approach import one_text_parser_untagged_chunk
from text_parser.sa_text_parser_tagged_dialog import one_text_parser_tagged, is_tagged
from text_parser.sa_text_parser_nlp_based import one_text_parser_nlp_based
from text_parser.utils import file_is_not_full, RESULT_DF_COLUMNS_NAMES



def main_text_parser(str_text):

    bstext = BeautifulSoup(str_text, 'html.parser')
    list_of_p_tags = bstext("p")

    if file_is_not_full(list_of_p_tags):

        result_df_from_text = pd.DataFrame(columns=RESULT_DF_COLUMNS_NAMES)

    else:

        if is_tagged(bstext):
            result_df_from_text = one_text_parser_tagged(str_text)
            print("+ tagged")
        else:
            result_df_from_text = one_text_parser_nlp_based(str_text)

    return result_df_from_text





if __name__=="__main__":

    from text_parser.utils import read_txt_file_with_decoding

    file_path = '../data/txt_data/inner/3000_num_13.txt'

    _str_text = read_txt_file_with_decoding(file_path)

    df = main_text_parser(_str_text)

    print()











