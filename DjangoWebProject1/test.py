
import os
import requests
from bs4 import BeautifulSoup
import hashlib
import os.path
import tqdm


global modpath, download_url
modpath = 'C:/Users/kross/Desktop/@MyMod'
download_url = 'http://127.0.0.1:8000/download-file/'


def get_input_values_from_div(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    center_div = soup.find('div', {'class': 'center'})
    input_values = []
    
    if center_div:
        input_tags = center_div.find_all('input')
        for input_tag in input_tags:
            name = input_tag.get('name')
            value = input_tag.get('value')
            input_values.append(name)
            input_values.append(value)
        
        return input_values
    else:
        return None


def delete_not_allowed_files(directory, allowed_files):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file not in allowed_files:
                os.remove(file_path)
                print(f"Файл {file_path} удален")



def download_file(url, destination_path):
      os.makedirs(destination_path, exist_ok=True)

      response = requests.get(url, stream=True)
      filename = response.headers.get('Content-Disposition').split('filename=')[1].strip('"')

      # Получаем размер файла
      file_size = int(response.headers.get('Content-Length', 0))

      # Создаем объект для отображения прогресса загрузки
      progress_bar = tqdm.tqdm(total=file_size, unit='B', unit_scale=True)

      # Сохраняем файл
      with open(os.path.join(destination_path, filename), 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
          if chunk:
            f.write(chunk)
            progress_bar.update(len(chunk))


def file_exists(filepath):
  """
  Проверяет, существует ли файл по указанному пути.

  Args:
    filepath: Путь к файлу.

  Returns:
    True, если файл существует, иначе False.
  """

  return os.path.isfile(filepath)

def get_file_extension(filepath):
  """
  Принимает название файла и возвращает его расширение.

  Args:
    Путь до файла.
  """

  return os.path.splitext(filepath)[1]


def check_keys(url, download_url, data):
    keys_path = modpath + '/keys'
    os.makedirs(keys_path, exist_ok=True) # Проверяем директорию мода, если не существует - создаем.
    items_to_delete = []
    for filename, md5 in data.items():
        file_path = keys_path + '' + '/' + filename
        file_extension = get_file_extension(file_path)
        if file_extension in ['.bikey']:
            if os.path.exists(keys_path):
                if file_exists(file_path):
                    with open(file_path, 'rb') as file:
                        file_md5 = hashlib.md5(file.read()).hexdigest()
                    if md5 and file_md5 == md5:
                        #print(f"Файл {filename} уже создан и он правильный.")
                        pass
                    else:
                        print(f"Файл {filename} поврежден, обновляю.")
                        os.remove(file_path)
                        download_file(download_url + filename + '/', keys_path)
                else:
                    print('Файл не существует, скачиваем')
                    download_file(download_url + filename + '/', keys_path)
            items_to_delete.append(filename)
    for el in items_to_delete:
        del data[el]
        #print(f'Элемент {el} удален')
    return data
def check_addons(url, download_url, data):
    addons_path = modpath + '/addons'
    os.makedirs(addons_path, exist_ok=True) # Проверяем директорию мода, если не существует - создаем.
    items_to_delete = []
    for filename, md5 in data.items():
        file_path = addons_path + '/' + filename
        
        file_extension = get_file_extension(file_path)
        if file_extension in ['.pbo', '.bisign']:
            if os.path.exists(addons_path):
                if file_exists(file_path):
                    with open(file_path, 'rb') as file:
                        file_md5 = hashlib.md5(file.read()).hexdigest()
                    if md5 and file_md5 == md5:
                        #print(f"Файл {filename} уже создан и он правильный.")
                        pass
                    else:
                        print(f"Файл {filename} поврежден, обновляю.")
                        os.remove(file_path)
                        download_file(download_url + filename + '/', addons_path)
                else:
                    print(file_path)
                    #print(f'Файл {filename} не существует, скачиваем')
                    download_file(download_url + filename + '/', addons_path) 
            items_to_delete.append(filename)
    for el in items_to_delete:
        del data[el]
        #print(f'Элемент {el} удален')
    return data


def check_files():
    """
     Проверяет правильность установки мода, если что-то не так - скачивает нужные файлы.

     Args:
        None
    """

    url = 'http://127.0.0.1:8000/file-list/'

    data = get_input_values_from_div(url)
    data = {data[i]: data[i+1] for i in range(0, len(data), 2)}

    os.makedirs(modpath, exist_ok=True) # Проверяем директорию мода, если не существует - создаем.
    delete_not_allowed_files(modpath, data.keys())
    data = check_addons(url, download_url, data)
    data = check_keys(url, download_url, data)

    for filename, md5 in data.items():
        file_path = modpath + '/' + filename
        file_extension = get_file_extension(file_path)
        if os.path.exists(modpath):
            if file_extension not in ['.pbo', '.bisign', '.bikey']:
                if file_exists(file_path):
                    with open(file_path, 'rb') as file:
                        file_md5 = hashlib.md5(file.read()).hexdigest()
                    if md5 and file_md5 == md5:
                       # print(f"Файл {filename} уже создан и он правильный.")
                       pass 
                    else:
                        print(f"Файл {filename} поврежден, обновляю.")
                        os.remove(file_path)
                        download_file(download_url + filename + '/', modpath)
                    
                else:
                    print(f'Файл {filename} не существует, скачиваем')
                    download_file(download_url + filename + '/', modpath)






def md5(fname):
    with open(fname, 'rb') as file:
        content = file.read()
        hash_value = hashlib.md5(content).hexdigest()
    return hash_value


def create_mod_info():
    os.makedirs(modpath, exist_ok=True) # Проверяем директорию мода, если не существует - создаем.
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '@MyMod')
    base_folder = os.path.dirname(os.path.dirname(base_dir))
    
    with open(os.path.join(base_folder, 'modinfo.txt'), 'w') as modfile:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                filepath = os.path.join(root, file)
                md5_hash = md5(filepath)
                modfile.write(f'{file} || {md5_hash}\n')


def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith("%2A"):
                new_file_name = file.replace("%2A", "")
                new_file_path = os.path.join(root, new_file_name)

                if os.path.exists(new_file_path):
                    os.remove(new_file_path)

                os.rename(os.path.join(root, file), new_file_path)

            if file.startswith("%3F"):
                old_path = os.path.join(root, file)
                new_filename = file.replace("%3F", "")
                new_path = os.path.join(root, new_filename)
                
                if os.path.exists(new_path):
                    os.remove(new_path)
                    
                os.rename(old_path, new_path)
                print(f"Файл {file} был переименован в {new_filename}")

        for subdir in dirs:
            rename_files(os.path.join(root, subdir))

while True:
    directory = input('Папка: ')
    rename_files(directory)



