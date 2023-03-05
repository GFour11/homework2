import os
import shutil
import sys

extensions={'Зображення':['jpeg', 'png', 'jpg', 'svg'],
           "Відео":['avi', 'mp4', 'mov', 'mkv'],
           "Документи":['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
           "Музика":['mp3', 'ogg', 'wav', 'amr'],
           "Архіви":['zip', 'gz', 'tar'],
           "Невідомі розширення":[]}


def create_dirs(path):
        os.mkdir(path + '\\Зображення')
        os.mkdir(path+ '\\Відео')
        os.mkdir(path+'\\Документи')
        os.mkdir(path+'\\Музика')
        os.mkdir(path+'\\Архіви')
        os.mkdir(path+'\\Невідомі розширення')


def normalize(word):
    result_name=''
    dicti ={'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v', 'Г': 'G', 'г': 'g', 'Д': 'D', 'д': 'd',
 'Е': 'E', 'е': 'e', 'Ё': 'E', 'ё': 'e', 'Ж': 'J', 'ж': 'j', 'З': 'Z', 'з': 'z', 'И': 'I', 'и': 'i', 'Й': 'J', 'й': 'j', 'К': 'K', 'к': 'k', 'Л': 'L',
 'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n', 'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r', 'С': 'S', 'с': 's', 'Т': 'T',
 'т': 't', 'У': 'U', 'у': 'u', 'Ф': 'F', 'ф': 'f', 'Х': 'H', 'х': 'h', 'Ц': 'TS', 'ц': 'c', 'Ч': 'CH', 'ч': 'ch', 'Ш': 'SH', 'ш': 'sh',
 'Щ': 'SCH', 'щ': 'sch', 'Ъ': '', 'ъ': '', 'Ы': 'Y', 'ы': 'y', 'Ь': '', 'ь': '', 'Э': 'E', 'э': 'e', 'Ю': 'YU',
 'ю': 'yu', 'Я': 'YA', 'я': 'ya', 'Є': 'JE', 'є': 'je', 'І': 'I', 'і': 'i', 'Ї': 'JI', 'ї': 'ji', 'Ґ': 'G', 'ґ': 'g'}
    for i in word:
        if i not in dicti.values():
            if i in dicti.keys():
                result_name+=dicti[i]
            elif '0'<=i<='9':
                result_name+=i
            else:
                result_name+='_'
        else:
            result_name+=i
    return result_name


def get_subfolder_paths(path):
    subfolder_paths = [f.path for f in os.scandir(path) if f.is_dir()]
    return subfolder_paths

def get_file_paths(path):
    file_paths = [f.path for f in os.scandir(path) if not f.is_dir()]
    return file_paths

def sort_files(ls,path):
    file_paths = ls
    ext_list = list(extensions.items())
    lst=[]
    for file_path in file_paths:
        lst.append(file_path)
        extension = file_path.split('.')[-1]
        file_name = file_path.split('\\')[-1]
        normalize_name =file_name.split('.')
        normal= normalize(normalize_name[0])
        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                os.rename(file_path, f'{path}\\{ext_list[dict_key_int][0]}\\{normal}.{extension}')
                lst.remove(file_path)
    for i in lst:
        file_name=i.split('\\')[-1]
        os.rename(i, f'{path}\\Невідомі розширення\\{file_name}')


def get_subfolders(path):
    subfolders = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            subfolders.append(item_path)
            subfolders.extend(get_subfolders(item_path))
    return subfolders

def full_sort(path):
    m= get_subfolders(path)
    for i in m:
        new_path= i
        sort =sort_files(get_file_paths(new_path),path)

def dearchivator(path):
    way = f'{path}\\Архіви'
    j = get_file_paths(way)
    for i in j:
        name = i.split('\\')[-1]
        name=name.split('.')
        (os.mkdir(way + f'\\{normalize(name[0])}'))
        shutil.unpack_archive(i,  f'{way}\\{normalize(name[0])}')
        os.remove(i)

def folder_remover(path):
    list_with_folders = get_subfolders(path)
    list_with_folders.reverse()
    for i in list_with_folders:
        name = i.split('\\')[-1]
        if name not in extensions.keys():
            if len(os.listdir(i))==0:
                os.rmdir(i)

def annotation_file(path):
    message=''
    for i in os.listdir(path):
        name = i.split('\\')[-1]
        message+=f'{name}:\n'
        for k in os.listdir(f'{path}\\{i}'):
                file_name = k.split('\\')[-1]
                message += f'--{file_name}\n'
    with open (f'{path}\\annotation.txt', 'x') as file:
        file.write(message)


def cleaner():
    path = sys.argv[1]
    if os.path.isdir(path):
        create_new_dirs= create_dirs(path)
        first_sort=sort_files(get_file_paths(path), path)
        second_sort = full_sort(path)
        archives_unpacker= dearchivator(path)
        clean=folder_remover(path)
        result_file=annotation_file(path)
        print('Ваші файли відсортовано')
    else:
        print("Шлях до папки вказано не вірно")

