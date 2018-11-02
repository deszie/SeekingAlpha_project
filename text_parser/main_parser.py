from bs4 import BeautifulSoup
import pandas as pd

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

    ### TypeError: unsupported operand type(s) for -: 'NoneType' and 'int' ----done except

    # file_path = '../data/txt_data/outer/770-1046/850_num_12.txt'
    # file_path = '../data/txt_data/outer/3560-4824/4689_num_7.txt'

    ### ValueError: not enough values to unpack (expected 2, got 0) ----not done

    # file_path = '../data/txt_data/inner/3087_num_20.txt'
    # file_path = '../data/txt_data/inner/3308_num_10.txt'
    # file_path = '../data/txt_data/inner/3308_num_6.txt'
    # file_path = '../data/txt_data/outer/770-1046/882_num_25.txt'
    # file_path = '../data/txt_data/outer/1900-2721/2227_num_29.txt'
    # file_path = '../data/txt_data/outer/1900-2721/2552_num_6.txt'
    # file_path = '../data/txt_data/outer/2721-3560/2876_num_25.txt'
    # file_path = '../data/txt_data/outer/2721-3560/2877_num_23.txt'
    # file_path = '../data/txt_data/outer/2721-3560/3358_num_6.txt'
    # file_path = '../data/txt_data/outer/2721-3560/3525_num_1.txt'
    # file_path = '../data/txt_data/outer/3560-4824/3578_num_2.txt'
    # file_path = '../data/txt_data/outer/3560-4824/3578_num_6.txt'
    # file_path = '../data/txt_data/outer/3560-4824/3647_num_18.txt'
    # file_path = '../data/txt_data/outer/3560-4824/3663_num_6.txt'
    # file_path = '../data/txt_data/outer/3560-4824/3670_num_3.txt'
    # file_path = '../data/txt_data/outer/3560-4824/3794_num_22.txt'
    # file_path = '../data/txt_data/outer/3560-4824/3997_num_3.txt'
    # file_path = '../data/txt_data/outer/3560-4824/4497_num_22.txt'
    # file_path = '../data/txt_data/outer/3560-4824/4578_num_26.txt'
    # file_path = '../data/txt_data/outer/3560-4824/4772_num_10.txt'
    # file_path = '../data/txt_data/outer/3560-4824/4784_num_2.txt'
    # file_path = '../data/txt_data/outer/3560-4824/4789_num_8.txt'
    # file_path = '../data/txt_data/outer/3560-4824/4800_num_27.txt'
    # file_path = '../data/txt_data/outer/3560-4824/4824_num_1.txt'
    # file_path = '../data/txt_data/outer/3560-4824/4824_num_17.txt'
    # file_path = '../data/txt_data/outer/3560-4824/4824_num_19.txt'

    ### TypeError: unorderable types: int() > NoneType() ----partially (without strong part)

    # file_path = '../data/txt_data/outer/3560-4824/4309_num_0.txt'
    # file_path = "../data/txt_data/inner/3052_num_10.txt"


    # file_path = "../data/txt_data/outer/1900-2721/2041_num_29.txt"
    # file_path = "../data/txt_data/outer/1900-2721/1946_num_14.txt"
    # file_path = "../data/txt_data/outer/1242-1894/1871_num_24.txt"
    # file_path = "../data/txt_data/outer/1-526/191_num_4.txt"
    # file_path = "../data/txt_data/outer/1900-2721/2192_num_1.txt"


    # file_path = "../data/txt_data/outer/1900-2721/2149_num_19.txt"
    # file_path = "../data/txt_data/outer/1900-2721/2151_num_20.txt"
    # file_path = "../data/txt_data/outer/1900-2721/2156_num_7.txt"
    # file_path = "../data/txt_data/outer/1900-2721/2189_num_12.txt"
    file_path = "../data/txt_data/outer/3560-4824/4434_num_1.txt"
    # file_path = "../data/txt_data/outer/3560-4824/4436_num_22.txt"

    _str_text = read_txt_file_with_decoding(file_path)

    bstext = BeautifulSoup(_str_text, 'html.parser')
    list_of_bs_p_tags = bstext('p')

    df = main_text_parser(_str_text)

    print()




