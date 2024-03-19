import configparser
import api

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    token_ya = config['yandex']['token']
    token_vk = config['vk']['token']
    user_id = config['vk']['user_id']

    vk_api = api.VkApi(token_vk)
    photos = vk_api.get_profile_photos(user_id)

    yandex_api = api.YandexDiskApi(token_ya)

    while True:
        folder_path = input('Folder to save profile photos in: ')
        response = yandex_api.create_folder(folder_path)
        if response.get('error') == 'DiskPathPointsToExistentDirectoryError':
            choice = input(f'Folder "{folder_path}" already exists, really use it? (yes/no): ')
            if choice.lower().startswith('y'):
                break
            else:
                continue
        break

    for photo in photos:
        file_name = f'{photo["id"]}.jpg'
        file_path = f'{folder_path}/{file_name}'
        yandex_api.upload_file_from_url(file_path, photo['url'])
