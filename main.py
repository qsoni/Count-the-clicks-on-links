import argparse
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
import requests


def shorten_link(headers, link):
  body = {
    'long_url': link
  }
  url = 'https://api-ssl.bitly.com/v4/bitlinks'
  response = requests.post(url, headers=headers, json=body)
  response.raise_for_status()
  return response.json()['id']


def count_clicks(headers, bitlink):
  url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
  response = requests.get(url, headers=headers)
  response.raise_for_status()
  clicks_count = response.json()
  return clicks_count['total_clicks']
  

def is_bitlink(headers, link):
  url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
  response = requests.get(url, headers=headers)
  return response.ok


if __name__ == '__main__':

  load_dotenv()

  bitly_token = os.getenv('BITLY_TOKEN')

  headers = {
    'Authorization': f'Bearer {bitly_token}'
  }

  parser = argparse.ArgumentParser(
    description='Сокращение ссылок'
  )
  parser.add_argument('user_link', help='Ваша ссылка')
  args = parser.parse_args()
  user_link = args.user_link

  parsed_user_link = urlparse(user_link)

  user_link_netloc_and_path = f'{parsed_user_link.netloc}{parsed_user_link.path}'
  if is_bitlink(headers, user_link_netloc_and_path):
    try:
      print(count_clicks(headers, user_link_netloc_and_path))
    except requests.exceptions.HTTPError:
      
      print('ошибка в подсчёте кликов по ссылке')
  else:
    try:
      print(shorten_link(headers, user_link))
    except requests.exceptions.HTTPError:
      
      print('ошибка в сокращении ссылки')