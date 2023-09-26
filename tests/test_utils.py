import pytest

from src.utils.utils import *
from src.constants.constants import *


@pytest.fixture
def coll():
    return [
        {"id": 1, "state": "executed"},
        {"id": 1.1, "state": ""},
        {"id": 1.2},
        {"id": 2, "state": "cancelled"},
        {"id": 3, "state": "executed"},
        {"id": 4, "state": "cancelled"},
        {"id": 5, "state": "executed"},
        {"id": 6, "state": "executed"},
        {"id": 7, "state": "executed"},
        {"id": 8, "state": "executed"},
        ]


def test__read_json():
    assert read_json("src/json_dir/test_2.json") == {"test":  "test"}


@pytest.mark.parametrize('list_, expected', [
    (
            [{"date": "2017-07-12T08:11:47.735774"},
             {"date": "2019-07-12T08:11:47.735774"},
             {"date": "2018-07-12T08:11:47.735774"},
             ],
            [{"date": "2019-07-12T08:11:47.735774"},
             {"date": "2018-07-12T08:11:47.735774"},
             {"date": "2017-07-12T08:11:47.735774"}
             ]
    ),
    (
            [{"date": "2017-07-12T08:11:47.735774"},
             {"date": "2000-07-12T08:11:47.735774"},
             {"date": "2000-07-12T08:11:47.735774"},
             ],
            [{"date": "2017-07-12T08:11:47.735774"},
             {"date": "2000-07-12T08:11:47.735774"},
             {"date": "2000-07-12T08:11:47.735774"}
             ]
    ),
    (
            [{"date": "2019-07-12T08:11:47.735774"},
             {"date": "2019-07-12T08:11:47.735775"},
             {"date": "2019-07-12T08:11:47.735776"},
             ],
            [{"date": "2019-07-12T08:11:47.735776"},
             {"date": "2019-07-12T08:11:47.735775"},
             {"date": "2019-07-12T08:11:47.735774"}
             ]
    )
])
def test__parse_data(list_, expected):
    assert parse_data(list_) == expected


def test__parse_date__value_error():
    with pytest.raises(ValueError):
        parse_data([{}, {"date": ""}])


def test__output_last_five(coll):
    assert output_last_five(coll) == [
        {"id": 1, "state": "executed"},
        {"id": 3, "state": "executed"},
        {"id": 5, "state": "executed"},
        {"id": 6, "state": "executed"},
        {"id": 7, "state": "executed"},
    ]


def test__hide_card_number():
    assert hide_card_number("Visa 1234000056780099", "Счет") == "Visa 1234 00** **** 0099"
    assert hide_card_number("Карта МИР 1234000056780099", "Счет") == "Карта МИР 1234 00** **** 0099"
    assert hide_card_number("Счет 1234000056780099", "Счет") == "Счет **0099"
    assert hide_card_number("Master Card 1234000056780099", "Счет") == "Master Card 1234 00** **** 0099"


def test__result_output():
    with open('src/json_dir/test.json', 'rt') as file:
        content = file.read()
        json_data = json.loads(content)
    assert result_output(json_data) == [
        '08.11.2018 Перевод организации\nСчет **8755 -> Счет **1744\n16872.46 USD',
        '15.08.2019 Перевод организации\nСчет **7907 -> Счет **9418\n31222.43 руб.',
        '03.02.2018 Открытие вклада\nСчет **8767\n90297.21 руб.',
        '17.08.2018 Перевод организации\nMaestro 1913 88** **** 1351 -> Счет **2427\n66906.45 USD']

