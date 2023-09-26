import json
from datetime import datetime
from src.constants.constants import *


def read_json(url_):
    """возвращает все данные json_dir-файла"""
    with open(url_, 'rt') as file:
        content = file.read()
        json_data = json.loads(content)

    return json_data


def parse_data(json_):
    """возвращает список операций, отсортированный по дате в обратной хронологии"""
    json_.sort(
        key=lambda operation:
        datetime.strptime(
            operation.get("date", DEFAULT_DATE),
            DATE_FORMAT
        )
        .timestamp() * 1000,
        reverse=True
    )
    return json_


def output_last_five(json_full_):
    """возвращает последние пять операций со статусом (state) Executed"""
    last_five_items = []
    count = 0
    for operation in json_full_:
        if (
                operation is not None
                and 'state' in operation.keys()
                and operation['state'].lower() == 'executed'
        ):
            last_five_items.append(operation)
            count += 1
            if count >= 5:
                break
        else:
            continue
    return last_five_items


def hide_card_number(card_number, bank_account):
    """принимает полное название карты/счета:
    - если это Счет (bank_account), то возвращает Счет **XXXX
    - если это карта, то возвращает Visa/Maestro XXXX XX** **** XXXX"""
    if bank_account in card_number:
        return f"""{bank_account} **{card_number[-4:]}"""
    else:
        card_name = ' '.join(card_number.split()[-3:-1])
        number = ''.join(card_number.split()[-1])
        return f"""{card_name} {number[:4]} {number[4:6]}** **** {number[-4:]}"""


def result_output(operation_list):
    """Возвращает список f-строк в формате:
    <дата перевода> <описание перевода>
    <откуда> -> <куда>
    <сумма перевода> <валюта>
    """
    result_output_list = []
    for operation in operation_list:
        keys_ = ["date", "description", "operationAmount"]
        if not all(key_ in operation.keys() for key_ in keys_):
            continue
        else:
            date_ = datetime.strptime(operation["date"], DATE_FORMAT).strftime("%d.%m.%Y")
            description = operation["description"]
            summa = operation["operationAmount"]["amount"]
            currency = operation["operationAmount"]["currency"]["name"]
            to_ = hide_card_number(operation["to"], "Счет")
            if "from" in operation.keys():
                from_ = hide_card_number(operation["from"], "Счет")
                result_output_list.append(
                    f'''{date_} {description}\n{from_} -> {to_}\n{summa} {currency}'''
                )
            else:
                result_output_list.append(
                    f'''{date_} {description}\n{to_}\n{summa} {currency}'''
                )
    return result_output_list
