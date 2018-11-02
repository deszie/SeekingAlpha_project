import os
import re
import pandas as pd
from collections import Counter



def _is_path_cls_msg(x):
    if "__main__ - ERROR - ERROR_CLASS:" in x:
        return True
    if "__main__ - ERROR - ERROR_MESSAGE:" in x:
        return True
    if "__main__ - ERROR - FILE_PATH_INFO:" in x:
        return True
    return False

def _pretiffy_triplet(x):
    re_class = re.findall(r"<class '.+'>", x[0])[0]
    re_msg = re.findall(r"ERROR_MESSAGE: .+", x[1])[0]
    re_path = re.findall(r"FILE_PATH_INFO: .+", x[2])[0]
    error = re_class[8:-2] + ": " + re_msg[15:]
    path = re_path[17:]
    return error, path




def parse_text_iterator_log(path):

    with open(path) as fl:
        log = fl.readlines()

    path_class_msg = list(filter(_is_path_cls_msg, log))

    # if len(path_class_msg)%3>0:
    #     raise ValueError()

    triplets = list(zip(*[iter(path_class_msg)] * 3))
    biplets = list(map(_pretiffy_triplet, triplets))

    df_errors = pd.DataFrame(biplets, columns=["ERROR", "PATH"])

    c = Counter(df_errors["ERROR"])
    df_freq = pd.DataFrame(list(c.items()), columns=["ERROR", "freq"]).sort_values("freq")

    errors_path_dict = {}
    for e in df_freq["ERROR"]:
        path_list = df_errors[df_errors["ERROR"]==e].PATH.tolist()
        errors_path_dict[e] = path_list

    return df_errors, df_freq, errors_path_dict







if __name__=="__main__":

    df_errors, df_freq, errors_path_dict = parse_text_iterator_log("../log/log_text_iterator.log")


    print()


for p in df_errors[df_errors['ERROR']=='ValueError: executives_flag > first_large_change']["PATH"]:
    print(p)



