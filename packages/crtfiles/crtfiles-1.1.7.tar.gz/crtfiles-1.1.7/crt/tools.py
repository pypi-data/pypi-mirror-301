import json
import os


def get_all_directories(path) -> list:
    files = os.listdir(path)
    return files


def get_file_nesting(nest, size_n) -> list:
    s_name = 0
    index = 0
    l_dir = []

    while index < len(nest):
        if nest[index] == '<':
            if nest[index+1] == '>':
                t_dir = ([], 1)
            else:
                t_dir = get_file_nesting(nest[index+1:], size_n)
            if type(t_dir) is tuple:
                list_dir, ind = t_dir
            else:
                list_dir = t_dir
                ind = size_n - index
            l_dir.append({f"{nest[s_name:index].replace(':', '')}": list_dir})
            index = index+ind + 1
            s_name = index+ind + 1
        if index+1 == len(nest):
            if (nest[s_name:index]):
                if (nest[index] == '>'):
                    l_dir.append(nest[s_name:index].replace(':', ''))
                else:
                    l_dir.append(nest[s_name:index+1].replace(':', ''))
                if index + 1 >= size_n:
                    return l_dir
                return (l_dir, index)
            return (l_dir)
        if index+1 > len(nest):
            if (nest[s_name:index]):
                l_dir.append(nest[s_name:index].replace(':', ''))
                if index + 1 >= size_n:
                    return l_dir
                return (l_dir, index)
            return (l_dir)
        if nest[index] == ':':
            if nest[s_name:index]:
                l_dir.append(nest[s_name:index].replace(':', ''))
            s_name = index
        if nest[index] == '>':
            if nest[s_name:index]:
                l_dir.append(nest[s_name:index].replace(':', ''))
            return (l_dir, index+1)
        index += 1
    return l_dir


def is_correct_request(s_name: str):

    incor_symbols = ['"', '|', '?', '*', ';', "'", ' ',]

    for sym in s_name:
        if sym in incor_symbols:
            return f"don't use signs {sym} in names"

    cont_l_b = s_name.count('<')
    cont_r_b = s_name.count('>')
    if cont_l_b == cont_r_b:
        return 1
    if cont_l_b < cont_r_b:
        return '<'
    if cont_l_b > cont_r_b:
        return '>'


def load_json_file(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as json_file:
        temp_file: dict = json.load(json_file)


def save_file(path: str, data: str) -> None:
    with open(path, 'w', encoding='utf-8') as file:
        file.write(data)
