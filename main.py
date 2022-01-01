import json
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    request_url = 'https://api-ssl.bitly.com/v4/shorten'
    data = json.dumps({"long_url": url})
    response = requests.post(url=request_url, headers=headers, data=data)
    response.raise_for_status()
    response = json.loads(response.text)
    bitlink = response['link']
    return bitlink


def count_clicks(token, link):
    headers = {'Authorization': f'Bearer {token}'}
    request_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    response = requests.get(url=request_url, headers=headers)
    response.raise_for_status()
    response = json.loads(response.text)
    clicks_count = response['total_clicks']
    return clicks_count


def is_bitlink(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    parsed_url = urlparse(url)
    bitlink = parsed_url.netloc + parsed_url.path
    request_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response = requests.get(url=request_url, headers=headers)
    if response.ok:
        return True
    return False


def main():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    # url = input('Введите ссылу: ')
    # url = "https://www.google.ru/"
    url = "https://bit.ly/3HylRIf"
    if is_bitlink(TOKEN, url):
        parsed_url = urlparse(url)
        link = parsed_url.netloc + parsed_url.path
        try:
            clicks_count = count_clicks(TOKEN, link)
        except requests.exceptions.HTTPError:
            print('Ошибка')
            return
        print('Кликов', clicks_count)

    else:
        try:
            bitlink = shorten_link(TOKEN, url)
        except requests.exceptions.HTTPError:
            print('Ошибка')
            return
        print('Битлинк', bitlink)


if __name__ == "__main__":
    main()
