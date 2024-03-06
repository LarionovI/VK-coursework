import os
import configparser
import photo_collector


config = configparser.ConfigParser()
config.read('setting.ini')


def create_local_folder():  # Создание папок для сохранения данных
    if not os.path.exists('Backup_log'):
        os.mkdir('Backup_log')


create_local_folder()

if __name__ == '__main__':
    like_url = None
    token_ya = config['YA_key']['token_ya']
    token_vk = config['VK_key']['token_vk']
    user_id = config['VK_key']['user_id']
    vk = photo_collector.VK(token_vk, user_id)
    ya = photo_collector.Yandex(token_ya, vk.get_photos())
    print(ya.upload())
    # print(ya.create_folder())
