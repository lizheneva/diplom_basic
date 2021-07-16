import requests


class FotoVK():
    def __init__(self, vk_token):
        self.vk_token = vk_token


    def photos_profile_get(self, owner_id, album_id, count):
        resul_link_dict = []
        params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'count': count,
            'extended': 1,
            'lang ': 0,
            'access_token': self.vk_token,
            'v': 5.77,

        }
        href = requests.get(
            'https://api.vk.com/method/photos.get', params).json()
        for photo in href['response']['items']:
            resul_link_dict += [{'file_name': f'{photo["likes"]["count"]}.jpg',
                                 'size': photo['sizes'][-1]['type'],
                                 'url': photo['sizes'][-1]['url']}]

        return resul_link_dict

    def albums_dict(self, owner_id):
        resul_link_dict = {}
        params = {
            'owner_id': owner_id,
            'need_system': 1,
            'lang ': 0,
            'access_token': self.vk_token,
            'v':  '5.30',
        }
        req = requests.get(
            'https://api.vk.com/method/photos.getAlbums', params).json()
        for aldum in req['response']['items']:
            resul_link_dict.update({aldum['id']: aldum['title']})
        return resul_link_dict