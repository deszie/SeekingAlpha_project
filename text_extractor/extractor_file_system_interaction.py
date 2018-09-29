import os
import pandas as pd

from text_parser.utils import read_txt_file_with_decoding, read_txt_file

EXTRACTOR_FS_INTERACTION_CWD = os.path.dirname(os.path.realpath(__file__))

def collect_txts_fs():
    folders_cur_paths = [
        '../data/txt_data/inner/',
        '../data/txt_data/outer/1-526/',
        '../data/txt_data/outer/770-1046/',
        '../data/txt_data/outer/1047-1241/',
        '../data/txt_data/outer/1242-1894/',
        '../data/txt_data/outer/1900-2721/',
        '../data/txt_data/outer/2721-3560/',
        '../data/txt_data/outer/3560-4824/'
    ]
    folders = [os.path.join(EXTRACTOR_FS_INTERACTION_CWD, folder) for folder in folders_cur_paths]
    for folder in folders:
        for file_path in list(map(lambda x: folder + x, os.listdir(folder))):
            if ".DS_Store" not in file_path:
                str_txt_text = read_txt_file_with_decoding(file_path)
                if len(str_txt_text)>10:
                    yield file_path, str_txt_text




if __name__=="__main__":

    for t in collect_txts_fs():
        print(t)

    # folders = [
    #     '../data/txt_data/inner/',
    #     '../data/txt_data/outer/1-526/',
    #     '../data/txt_data/outer/770-1046/',
    #     '../data/txt_data/outer/1047-1241/',
    #     '../data/txt_data/outer/1242-1894/',
    #     '../data/txt_data/outer/1900-2721/',
    #     '../data/txt_data/outer/2721-3560/',
    #     '../data/txt_data/outer/3560-4824/'
    # ]
    #
    # alltxts = []
    # for f in folders:
    #     alltxts += list(map(lambda x: f + x, os.listdir(f)))
    #
    # print(len(alltxts))

    # from text_parser.utils import file_is_not_full
    # from text_parser.sa_text_parser_tagged_dialog import is_tagged
    # from bs4 import BeautifulSoup
    #
    # for file_path, str_text in collect_txts_fs():
    #
    #     bstext = BeautifulSoup(str_text, 'html.parser')
    #     list_of_p_tags = bstext("p")
    #
    #     print(file_path)
    #
    #     if not file_is_not_full(list_of_p_tags):
    #         if not is_tagged(bstext):
    #
    #             print("untagged")
    #
    #             with open("../data/utagged_files.txt", "a") as f:
    #                 f.write(file_path + "\n")




