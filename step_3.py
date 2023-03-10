import os
import json
import csv
import gspread
from tqdm import tqdm

# gs = gspread.service_account(filename='gsheets.json')  # подключаем файл с ключами и пр.
# sh = gs.open_by_key('14QrehUZfY9SkQwl85OjX-l2l8Avt6o6QWh4kowKqboI')  # подключаем таблицу по ID
# worksheet = sh.worksheet('Лист 2')  # получаем первый лист

# Считываем все файлы json в папке result и объединяем данные в один список
file_path = 'encoded'
prepared_data = []
for file_name in tqdm(os.listdir(file_path), desc='Собираем файлы из папки'):
    if file_name.endswith('.json'):

        with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as f:
            data = json.load(f)
            prepared_data.extend(data)

# Обработка данных для записи в гугл таблицу
for data_item in tqdm(prepared_data, desc='Подготавливаем данные'):
    # Добавляем недостающие поля, если они отсутствуют
    # if 'title' not in data_item:
    #     data_item['title'] = ''
    # if 'chat_id_or_url' not in data_item:
    #     data_item['chat_id_or_url'] = ''
    if 'post_id' not in data_item:
        data_item['post_id'] = ''
    # if 'date' not in data_item:
    #     data_item['date'] = ''
    # if 'content' not in data_item:
    #     data_item['content'] = ''
    # if 'image_url' not in data_item:
    #     data_item['image_url'] = ''
    # if 'video_preview' in data_item:
    #     data_item['video_preview'] = ''
    # if 'views' in data_item:
    #     data_item['views'] = ''
    

    # Преобразуем дату в нужный формат
    date_str = data_item['date'][:10]
    date_parts = date_str.split('-')
    data_item['date'] = str(f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}")



with open('data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['title', 'chat_id_or_url','post_id', 'date', 'content', 'image_url', 'video_preview', 'views'])
    for row in tqdm(prepared_data, desc='Записываем данные в файл data.csv'):
        writer.writerow([row['title'], row['chat_id_or_url'], row['post_id'], row['date'], row['content'], row['image_url'], row['video_preview'], row['views']])


# Запись данных в таблицу
# Кортеж полей, которые мы хотим сохранить в таблице
# FIELDS_TO_SAVE = ('url', 'date', 'content', 'outlinks', 'linkPreview', 'image_url', 'video_preview', 'video_link', 'views')

# existing_headers = worksheet.row_values(1)
# for field in FIELDS_TO_SAVE:
#     if field not in existing_headers:
#         worksheet.update_cell(1, len(existing_headers) + 1, field.capitalize())
#         existing_headers.append(field)

# # Запись данных в таблицу
# for item in prepared_data:
#     row = []
#     for field in FIELDS_TO_SAVE:
#         row.append(item.get(field, "")) # Если значение отсутствует, используем пустую строку
#         #print(row)
#     worksheet.append_row(row)


# worksheet.clear() # Очистка листа перед записью данных
# worksheet.append_rows(prepared_data, value_input_option='USER_ENTERED') # Запись данных в таблицу
