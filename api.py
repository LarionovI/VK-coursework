import json
import os
import requests
# import urllib.parse


class VkApi:
    base_url = 'https://api.vk.com/method'

    def __init__(self, token: str):
        self.token = token
        self.base_params = {
            'access_token': self.token,
            'v': '5.199'
        }

    def get_profile_photos(self, owner_id: str):
        url = f'{self.base_url}/photos.get'
        params = {
            **self.base_params,
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': '1',
        }
        response = requests.get(url=url, params=params).json()

        items = response['response']['items']
        photos = [{
            'id': photo['id'],
            'likes': photo['likes']['count'],
            'url': max(photo['sizes'], key=lambda size: size['width'] * size['height'])['url'],
        } for photo in items]

        if not os.path.exists('log'):
            os.mkdir('log')
        with open('log/photos.json', 'w') as file:
            json.dump(photos, file, indent=4)

        return photos


class YandexDiskApi:
    base_url = 'https://cloud-api.yandex.net/v1/disk'

    def __init__(self, token: str):
        self.token = token
        self.base_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder(self, path: str):
        url = f'{self.base_url}/resources'
        params = { 'path': path }
        response = requests.put(url=url, headers=self.base_headers, params=params)

        return response.json()
    
    def upload_file_from_url(self, file_path: str, file_url: str):
        url = f'{self.base_url}/resources/upload'
        params = {
            # quoting here is an error, as it will result in a double quote
            # quoting is done automatically by the 'requests' module
            # 'path': urllib.parse.quote(file_path, encoding='utf-8', errors=None),
            # 'url': urllib.parse.quote_plus(file_url, encoding='utf-8', errors=None),
            'path': file_path,
            'url': file_url,
        }
        response = requests.post(url=url, headers=self.base_headers, params=params)

        return response.json()


if __name__ == '__main__':
    import configparser
    config = configparser.ConfigParser()
    config.read('settings.ini')

    vk_api = VkApi(config['vk']['token'])
    # response = vk_api.get_profile_photos('max_tigerrr')
    # response = vk_api.get_profile_photos('121296382') # kezos
    # response = vk_api.get_profile_photos('79795768') # shadou
    response = vk_api.get_profile_photos('336658543')
    print(response)

    # yandex_api = YandexDiskApi(config['yandex']['token'])
    # # response = yandex_api.create_folder('some_path')
    # response = yandex_api.upload_file_from_url('some_path/loh.jpeg', 'https://i.imgur.com/h2vbu6N.jpeg')
    # response = yandex_api.upload_file_from_url('some_path/loh.jpeg', 'https://sun9-67.userapi.com/c11422/u79795768/-6/x_5f5f517f.jpg')
    # print(response)
