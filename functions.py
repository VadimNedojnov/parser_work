import random
from time import sleep
from user_agent import generate_user_agent
import requests
from bs4 import BeautifulSoup
import json


HOST = 'https://www.work.ua'
ROOT_PATH = '/ru/jobs/'


def save_info(array: list) -> None:
    with open('workua.txt', 'a') as file:
        for line in array:
            file.write(' | '.join(line) + '\n')


def save_info_json(data: dict) -> None:
    with open('workua.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write('\n')


def random_sleep():
    sleep(random.randint(3, 4))


def user_agent_generator():
    user_agent = generate_user_agent()
    headers = {
        'User-Agent': user_agent,
    }
    return headers


def vacancy_review(href, headers):
    response_additional = requests.get(HOST + ROOT_PATH + href.replace('/ru/jobs/', ''),
                                       headers=headers)
    html_additional = response_additional.text
    soup_additional = BeautifulSoup(html_additional, 'html.parser')
    return soup_additional
