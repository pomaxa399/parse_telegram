import json
import subprocess
import re
#from bs4 import BeautifulSoup

# Список каналов телеграм https://t.me/ai_university_web
tgchannels = ['ai_university_web']

# Дата в формате 'yyyy-mm-dd', с которой интересуют посты и до сегодня
start_date = '2023-02-22'
# Парсит с телеграм канала последние num-res кол-во постов
max_res = True
num_res = 10

# Список файлов для фильтрации по датам
files_json = []

def fix_content(files_json):
    for file in files_json:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                # получение значения поля "content"
                content = item['content']
                if content is not None:
                    content = re.sub(r'<[^>]+>', '', content)
                    content = content.replace('\n', ' ').strip()
                    content = ' '.join(content.split())
                    item['content'] = content

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)



# Парсим телеграм каналы
def parse_tg(*args):
    for channel in tgchannels:
        if max_res:
            result = subprocess.run(['snscrape', '--max-results', str(num_res), '--jsonl', 'telegram-channel', channel],
                                    capture_output=True, text=True)
        else:
            result = subprocess.run(['snscrape', '--jsonl', 'telegram-channel', channel], capture_output=True, text=True)
        
        with open(channel+'.json', 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        file = channel+'.json'
        files_json.append(file)
    return files_json


# Приведение данных контента к нормальной кодировке
def fix_encoding(files_json):
    for file in files_json:
        with open(file, 'r', encoding='cp1251') as f:
            decoded_data = []
            for line in f:
                data = json.loads(line)
                decoded_data.append(data)

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(decoded_data, f, ensure_ascii=False, indent=4)
        
        fix_content(files_json)
    


# Фильтрация данных от интересующей даты
def sorted_data(*args):
    for file in files_json:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        start = start_date
        filtered_data = [d for d in data if d['date'] >= start]

        with open('filtered_'+file, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)


def main():
    parse_tg(tgchannels, max_res, num_res)
    fix_encoding(files_json)
    sorted_data(files_json, start_date)

if __name__ == '__main__':
    main()
