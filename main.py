import datetime
from progress.bar import FillingSquaresBar
from yadi import YandexDisk
from vk import FotoVK



if __name__ == '__main__':
    TOKEN_VK = input("Введите токен VK: ")
    TOKEN_YA = input("Введите токен Яндекс Диск: ")
    vk_user_id = input("Введите id пользователя")

    vk = FotoVK(TOKEN_VK)
    ya = YandexDisk(TOKEN_YA)
    now_date = datetime.now().date()
    choice_albums = {}
    n = 1

    for id_alnum, name_album in vk.albums_dict(vk_user_id).items():
        choice_albums.update({n: {'id_alnum': id_alnum,
                                  'name_album': name_album}})
        print(f'{n}: {name_album}')
        n += 1

    while True:
        chosen = int(
            input('Выберите номер альбома: '))
        if chosen in [x for x in range(1, len(choice_albums))]:
            break
        else:
            print('Данного варианта не существует\nПопробуйте снова: ')

    folder_in_ya = f'{now_date}_vk'
    if ya.create_folder(folder_in_ya) == 201:
        names = [name['name']
                 for name in ya.get_files_list(folder_in_ya)['_embedded']['items']]
        vk_dic_photo = vk.photos_profile_get(vk_user_id,
                                             choice_albums[chosen]['id_alnum'],
                                             5)
        bar = FillingSquaresBar('Идет скачивание', max=len(vk_dic_photo))

        for photo in vk_dic_photo:

            if photo["file_name"] not in names:
                disk_file_path = f'{folder_in_ya}/{photo["file_name"]}'
            else:
                answer = input(f'Файл с именем {photo["file_name"]} уже существует\nЗаменить его?')
                if answer == "Да":
                    disk_file_path = f'{str(folder_in_ya)}/{photo["file_name"]}'
                else:
                    bar.next()
                    continue
            ya.upload_file_link_to_disk(disk_file_path, photo['url'])
            bar.next()
        bar.finish()
        print('Сделано')
    else:
        print('Ошибка создания папки в Яндекс Диске')


