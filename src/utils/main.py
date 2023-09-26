from utils import *

# Получаем данные из operations.json
json_full = read_json(JSON_PATH)

# Сортируем полученные данные по дате (в обратном хронологическом порядке)
parse_data(json_full)

# Выводим искомый результат - 5 операций вида:
# 14.10.2018 Перевод организации
# Visa Platinum 7000 79** **** 6361 -> Счет **9638
# 82771.72 руб.
print(*result_output(output_last_five(json_full)), sep="\n\n")
