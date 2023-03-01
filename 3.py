import os
import json
import csv
import gspread

gs = gspread.service_account(filename='gsheets.json')  # подключаем файл с ключами и пр.
sh = gs.open_by_key('14QrehUZfY9SkQwl85OjX-l2l8Avt6o6QWh4kowKqboI')  # подключаем таблицу по ID
worksheet = sh.worksheet('Лист 2')  # получаем первый лист

# Считываем все файлы json в папке result и объединяем данные в один список
file_path = 'encoded'
prepared_data = []
for file_name in os.listdir(file_path):
    if file_name.endswith('.json'):
        print(file_name)
        with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as f:
            data = json.load(f)
            prepared_data.extend(data)
print(prepared_data)
# Обработка данных для записи в гугл таблицу
for data_item in prepared_data:
    # Добавляем недостающие поля, если они отсутствуют
    if 'url' not in data_item:
        data_item['url'] = ''
    if 'content' not in data_item:
        data_item['content'] = ''
    if 'image_url' not in data_item:
        data_item['image_url'] = ''
    if 'views' not in data_item:
        data_item['views'] = ''
    # if 'description' not in data_item:
    #     data_item['description'] = ''
    # if 'siteName' not in data_item:
    #     data_item['siteName'] = ''
    # if 'title' not in data_item:
    #     data_item['title'] = ''
    if 'video_preview' not in data_item:
        data_item['video_preview'] = ''
    # if 'linkPreview' not in data_item:
    #     data_item['linkPreview'] = ''
    if 'video_link' not in data_item:
        data_item['video_link'] = ''
    if 'outlinks' in data_item:
        data_item['outlinks'] = ", ".join(data_item['outlinks'])
    else:
        data_item['outlinks'] = ''

    # Преобразуем дату в нужный формат
    date_str = data_item['date'][:10]
    date_parts = date_str.split('-')
    data_item['date'] = str(f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}")



with open('data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['url', 'date', 'content', 'outlinks', 'image_url', 'video_preview', 'video_link', 'views'])
    for row in prepared_data:
        writer.writerow([row['url'], row['date'], row['content'], row['outlinks'], row['image_url'], row['video_preview'], row['video_link'], row['views']])


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
