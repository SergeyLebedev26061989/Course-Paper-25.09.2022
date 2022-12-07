import requests, time
from collections import Counter
from tqdm import tqdm
from pprint import pprint

class VK():
    def get_vk_photo(id, token, album_id='profile'):
        url_vk = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': token,
            'v': '5.131',
            'owner_id': id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1'
        }
        response = requests.get(url=url_vk, params=params)
        photo = response.json()
        return photo['response']

    def get_size_photo(photo_dict):
        temp_dict_photo = {}
        necessary_photo = {}
        necessary_photo['likes'] = photo_dict['likes']['count']
        for photo in photo_dict['sizes']:
            temp_dict_photo[photo['type']] = photo['url']
        if 'z' in temp_dict_photo:
            necessary_photo['size'] = 'z'
            necessary_photo['url'] = temp_dict_photo['z']
        elif 'y' in temp_dict_photo:
            necessary_photo['size'] = 'y'
            necessary_photo['url'] = temp_dict_photo['y']
        elif 'x' in temp_dict_photo:
            necessary_photo['size'] = 'x'
            necessary_photo['url'] = temp_dict_photo['x']
        return necessary_photo

class Yandex():
    def get_folder(name_folder='vk_photo'):
        url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {ya_token}'
        }
        params_ya = {
            'path': name_folder
        }
        response = requests.put(url=url_ya, headers=headers, params=params_ya)
        return

    def upload_photo(list_photo, token, folder='vk_photo'):
        url_ya = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token}'
        }
        for dict_photo in tqdm(list_photo):
            params = {
                'path': f'{folder}/{dict_photo["file_name"]}',
                'url': dict_photo['url']
            }
            response = requests.post(url=url_ya, headers=headers, params=params)
            time.sleep(0.2)
        return

    def name_file(number, photo_in_vk):
        photo_list = []
        count_photo = []
        while number != 0:
            photo = VK.get_size_photo(photo_in_vk[number - 1])
            photo['file_name'] = f'{photo["likes"]}.jpg'
            photo_list.append(photo)
            number -= 1
        for photo_vk in photo_list:
            count_photo.append(photo_vk['file_name'])
        count_name_photo = Counter(count_photo)
        for file, count_number in dict(count_name_photo).items():
            if count_number == 1:
                del count_name_photo[file]
        for photo_dict in photo_list:
            if photo_dict['file_name'] in count_name_photo:
                photo_dict['file_name'] = f'{photo_dict["likes"]}{photo_dict["date"]}.jpg'
        return photo_list

if __name__ == '__main__':
    vk_token = ''
    ya_token = ''
    folder_name = 'photos_from_vk'
    Yandex.get_folder(folder_name)
    id_client = input('Введите id пользователя VK: ')
    vk = VK.get_vk_photo(id_client, vk_token)
    count = vk['count']
    vk_photo = vk['items']
    user_number_photo = int(input('Введите количество фото которые хотите загрузить: '))
    if user_number_photo <= count:
        files = Yandex.name_file(user_number_photo, vk_photo)
    else:
        files = Yandex.name_file(count, vk_photo)
    Yandex.upload_photo(files, ya_token, folder_name)