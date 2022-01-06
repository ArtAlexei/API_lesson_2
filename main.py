import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    request_url = 'https://api-ssl.bitly.com/v4/shorten'
    param = {"long_url": url}
    response = requests.post(url=request_url, headers=headers, json=param)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, link):
    headers = {'Authorization': f'Bearer {token}'}
    request_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    response = requests.get(url=request_url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    parsed_url = urlparse(url)
    bitlink = parsed_url.netloc + parsed_url.path
    request_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response = requests.get(url=request_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.getenv("BITLY_GENERIC_ACCESS_TOKEN")
    url = input('Введите ссылу: ')
    if is_bitlink(token, url):
        parsed_url = urlparse(url)
        link = f'{parsed_url.netloc}{parsed_url.path}'
        try:
            clicks_count = count_clicks(token, link)
        except requests.exceptions.HTTPError:
            print('Ошибка')
        else:
            print('Кликов', clicks_count)

    else:
        try:
            bitlink = shorten_link(token, url)
        except requests.exceptions.HTTPError:
            print('Ошибка')
        else:
            print('Битлинк', bitlink)


if __name__ == "__main__":
    main()
