import os
from crt.templates import get_fiil_templates, get_templates
from crt.tools import get_all_directories, get_file_nesting, is_correct_request, save_file


def c_f(t_str_names,  ext=None, name=None):
    if type(t_str_names) is dict:
        for key in t_str_names:
            if (name):
                full_name = name+"\\"+key
                if not os.path.isdir(full_name):
                    os.system(f"mkdir {full_name}")
            else:
                full_name = key
                if not os.path.isdir(full_name):
                    os.system(f"mkdir {full_name}")
            for file in t_str_names[key]:
                if type(file) is str:
                    if full_name and file:
                        file_name = f"{full_name}\{file}.{ext}" if ext else f"{full_name}\{file}"
                    elif file:
                        file_name = f"{file}.{ext}" if ext else f"{file}"
                    else:
                        file_name = None
                    if file_name:
                        if not os.path.isfile(file_name):
                            os.system(f"type NUL > {file_name}")
                else:
                    c_f(t_str_names=file,  ext=ext, name=full_name)
    else:
        for file in t_str_names:
            if (name):
                if not os.path.isdir(name):
                    os.system(f"mkdir {full_name}")
                full_name = name+'\\'
            else:
                full_name = ""
            if type(file) is str:
                if (full_name):
                    file_name = f"{full_name}\{file}.{ext}" if ext else f"{full_name}\{file}"
                else:
                    file_name = f"{file}.{ext}" if ext else f"{file}"
                if not os.path.isfile(file_name):
                    os.system(f"type NUL > {file_name}")
            else:
                c_f(file, ext, full_name)


def c_d(l_str_names):
    if type(l_str_names) is dict:
        for key in l_str_names.keys():
            l_str_names[key] = c_d(l_str_names[key])
    else:
        for index in range(len(l_str_names)):
            if type(l_str_names[index]) is dict:
                l_str_names[index] = c_d(l_str_names[index])
            else:
                if not '.' in l_str_names[index] and l_str_names[index] != "LICENSE":
                    l_str_names[index] = {l_str_names[index]: []}
    return l_str_names


def crt_files(ext, t_str_names):
    ans = is_correct_request(t_str_names)
    if ans == 1:
        l_dir = get_file_nesting(t_str_names, len(t_str_names))
        c_f(l_dir, ext)
    elif ans == '>' or ans == '<':
        print(f"missing sign '{ans}' (use crt --help)")
    else:
        print(f"{ans} (use crt --help)")


def crt_dirs(t_str_names):
    all_directories = get_all_directories('.')
    for str_names in t_str_names:
        for dir_name in str_names.split(":"):
            if dir_name not in all_directories:
                os.system(f"mkdir {dir_name}")


def crt_temp(json_temp: dict):
    l_dir = c_d(json_temp)
    c_f(l_dir)


def fill_temp(d_temp):
    for file_path in d_temp.keys():
        print(file_path)
        code = d_temp[file_path].replace('/$$/', '\n')
        save_file(path=file_path, data=code)


def temp_is_exist(temp_name: str) -> bool:
    l_temp = get_templates(temp_name)
    if not l_temp:
        return False
    return l_temp


def fill_code_is_exist(temp_name: str):
    d_temp = get_fiil_templates(temp_name)
    if not d_temp:
        return False
    return True
