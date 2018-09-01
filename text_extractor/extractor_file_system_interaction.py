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

# for t in collect_txts():
#     print(t)

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








