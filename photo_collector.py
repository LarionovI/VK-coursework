import json
import requests
import time
import urllib.parse

import main

date = time.strftime("%H-%M-%S_%d-%m-%Y", time.localtime())
folder_name = str(input('Введите название папки для сохранения фото: '))


class VK:
    base_url = 'https://api.vk.com/method'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def assembling(self, method):  # Сборка ссылки
        return f'{self.base_url}/{method}'

    def params_vk(self):  # функция для получения обязательных параметров
        return {
            'access_token': self.token,
            'v': '5.199'
        }

    def get_photos(self):

        params = self.params_vk()
        params.update({'album_id': 'profile',  # добавление параметров к обязательным
                       'extended': '1'})

        if self.user_id.isdigit():  # проверка на введенный id либо screen_name
            params.update({'owner_id': self.user_id})
        else:
            params.update({'screen_name': self.user_id})

        response = requests.get(self.assembling('photos.get'), params=params).json()['response']['items']
        photo_info = []
        like_url = []
        count = 0

        for row in response:
            count += 1
            max_size = 0
            temp_dict = {}
            if row['likes']['count'] in temp_dict:  # условие для получения имени фото по лайкам, если нет like+data
                like = f'{row['likes']['count']} {date}'
            else:
                like = row['likes']['count']
            for size in row['sizes']:  # получение ссылки на фото максимального размера
                if size['height'] >= max_size:
                    max_size = size['height']
                    url = size['url']
                    temp_dict[like] = url
            like_url.append(temp_dict)
            info_size = {'file_name': f'{like}.png',
                         'size': row['sizes'][0]['type']}  # создание словаря для записи в json
            photo_info.append(info_size)
            with open("Backup_log/%s" % "log.json", "w") as file:  # запись логов по фото
                json.dump(photo_info, file, indent=4)
        return like_url


class Yandex:
    api_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token, like_url):
        self.token = token
        self.folder_name = folder_name
        self.like_url = like_url

    def create_folder(self):  # создание папки на яндекс диске с условием ошибки(уже существует)
        headers = {'Content-Type': 'application/json',
                   'Authorization': self.token}
        params = {'path': self.folder_name}
        response = requests.put(url=self.api_url, headers=headers, params=params).json()
        if 'error' in response:
            while response['error'] == 'DiskPathPointsToExistentDirectoryError':
                self.folder_name = str(input(f'Папка с именем "{self.folder_name}" уже существует, введите другое имя: '))
                params.update({'path': self.folder_name})
                response = requests.put(url=self.api_url, headers=headers, params=params).json()
                if 'error' not in response:
                    break
        return f'disk/{self.folder_name}/'

    def upload(self):  # загрузка фото в созданную папку
        headers = {'Content-Type': 'application/json',
                   'Authorization': self.token}
        name_f = self.create_folder()
        for row in self.like_url:   # не могу понять как составить путь до папки правильно, загружает только в корень!
            for file_name in row:
                link_photo = urllib.parse.quote_plus(row[file_name], encoding='utf-8', errors=None)
                url = self.api_url + '/upload?url=' + link_photo
                link_upl = urllib.parse.quote_plus(f'{file_name}.png', encoding='utf-8', errors=None)
                params = {'path': link_upl}
                requests.post(url=url, params=params, headers=headers)




