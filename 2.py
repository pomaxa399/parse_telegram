import json
import os
import subprocess
import re
from gsheet import links
from tqdm import tqdm

# Список каналов телеграм https://t.me/ai_university_web
tgchannels = links

# Дата в формате 'yyyy-mm-dd', с которой интересуют посты и до сегодня
start_date = '2023-01-01'
# Парсит с телеграм канала последние num-res кол-во постов
max_res = True
num_res = 100

# Список файлов для фильтрации по датам
# files_json = []
encoded_files = []
deleted_files = []
def remove_empty_files(deleted_files):

    for file in deleted_files:
        #if os.stat(file).st_size == 0:
            if os.path.exists(file):
                os.remove(file)


def fix_content(encoded_files):
    for file in tqdm(encoded_files, desc='Чистим поле контента', unit='file'):
    # for file in files_json[:]:
            
        with open(file, 'r', encoding='utf-8') as f:

            data = json.load(f)

            if not data:
                deleted_files.append(file)
                # encoded_files.remove(file)
                f.close()
                os.remove(file)
                continue

            for item in data:
                content = item['content']

                if content is not None:
                    content = re.sub(r'<[^>]+>', '', content)
                    content = content.replace('\n', ' ').strip()
                    content = ' '.join(content.split())
                    item['content'] = content

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    return deleted_files
    
# Парсим телеграм каналы
def parse_tg(*args):
    for channel in tqdm(tgchannels, total=len(tgchannels), desc="Парсим каналы"):
    # for channel in tgchannels:
        if max_res:
            result = subprocess.run(['snscrape', '--max-results', str(num_res), '--jsonl', 'telegram-channel', channel],
                                    capture_output=True, text=True)
        else:
            result = subprocess.run(['snscrape', '--jsonl', 'telegram-channel', channel], capture_output=True, text=True)
        if not os.path.exists('result'):
            os.mkdir('result')
        file_path = os.path.join('result', channel + '.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
    #     files_json.append(file_path)
    # return files_json



# Приведение данных контента к нормальной кодировке
def fix_encoding(output_folder='encoded'):
    file_path = 'result'
    fj = []
    for file_name in os.listdir(file_path):
        if file_name.endswith('.json'):
            fj.append(os.path.join(file_path, file_name))
    os.makedirs(output_folder, exist_ok=True)
    for file in tqdm(fj, desc='Исправляем кодировку', unit='file'):
        decoded_data = []
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    decoded_data.append(data)
                except json.JSONDecodeError:
                    pass

        # Формируем путь до закодированного файла в папке `output_folder`
        encoded_file_path = os.path.join(output_folder, os.path.basename(file))

        with open(encoded_file_path, 'w', encoding='utf-8') as f:
            json.dump(decoded_data, f, ensure_ascii=False, indent=4)
        
        encoded_files.append(encoded_file_path)

    return encoded_files
    

# Фильтрация данных от интересующей даты
def sorted_data(*args):
    file_path = 'encoded'
    ef = []
    for file_name in os.listdir(file_path):
        if file_name.endswith('.json'):
            # print(file_name)
            ef.append(os.path.join(file_path, file_name))
    for file in tqdm(ef, desc='Делаю выборку от назначенной даты', unit='file'):
    # for file in files_json:

        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        start = start_date
        filtered_data = [d for d in data if d['date'] >= start]

        if not filtered_data:
                # f.close()
                os.remove(file)
                continue

        if not os.path.exists('filtered_result'):
            os.mkdir('filtered_result')

        with open(os.path.join('filtered_result', 'filtered_'+os.path.basename(file)), 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)


def main():
    parse_tg(tgchannels, max_res, num_res)
    fix_encoding()
    # # remove_empty_files(deleted_files)
    fix_content(encoded_files)
    
    # # print(encoded_files)
    sorted_data(start_date)
    # # print(ef)
    # print(deleted_files)
    # print('Final')

if __name__ == '__main__':
    main()
