from pprint import pprint

import requests

class YandexDisk:

    def fotos_VK():
        VK_USER_ID = int(input('enter YOUR ID_VK: '))
        VK_TOKEN = input('enter YOUR token_VK: ')
        URL = 'https://api.vk.com/method/photos.get'

        params = {
            'owner_id': VK_USER_ID,
            'access_token': VK_TOKEN,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': '1',
            'v': '5.131'
        }
        photo = requests.get(URL, params=params).json()
        di_ = {}

        for f in photo['response']['items']:
            file_name = f['likes']['count']
            for i in f['sizes']:
                if i['type'] == 'z':
                    link = i['url']
                    di_[file_name] = [link]

        for foto, value in di_.items():
            result = uploader.upload_file_to_disk('NetologyVK/' + str(di_[foto]), str(di_[value]))

            return result


    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def upload_file_to_disk(self, file_path, photo_url):
        # YandexDisk.fotos_VK()
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": file_path,
                  "url": photo_url}
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.token)}
        response = requests.post(upload_url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

if __name__ == '__main__':
    token = input('введите свой TOKEN: ')
    uploader = YandexDisk(token)
    YandexDisk.fotos_VK()
    result = uploader.upload_file_to_disk('NetologyVK/' + str(foto), str(di_[foto]))




