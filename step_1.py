import gspread
from google.oauth2.service_account import Credentials

gs = gspread.service_account(filename='gsheets.json')  # подключаем файл с ключами и пр.
sh = gs.open_by_key('14QrehUZfY9SkQwl85OjX-l2l8Avt6o6QWh4kowKqboI')  # подключаем таблицу по ID
worksheet = sh.sheet1  # получаем первый лист


column_number = 2
link_values = worksheet.col_values(column_number)


links = []
for link in link_values[1:]:
    parts = link.split('/')
    last_part = parts[-1]
    if last_part.startswith('@'):
        last_part = last_part[1:]
    links.append(last_part)
print('Загружено ссылок для сбора данных:',len(links))