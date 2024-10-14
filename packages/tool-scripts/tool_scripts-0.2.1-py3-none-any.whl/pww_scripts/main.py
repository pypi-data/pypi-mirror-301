from pww_scripts.entity.Artist import Artist
from pww_scripts.entity.Info import Info
from pww_scripts.script import insert_spider_data
from pww_scripts.script.get_info_and_save import save_info
from pww_scripts.utils import *


# 通过文件夹名称获取信息 并保存到数据库
def save():
    folder = 'D:\\gitHub\\test'

    _list = os.listdir(folder)
    for f in _list:
        info = Info()
        info.path = os.path.join(folder, f)
        info.number = f
        save_info(info)


def scan():
    folder = 'D:\\mycode\\test'

    _list = os.listdir(folder)
    for f in _list:
        artist = Artist()
        artist.name = f
        artist.local_path = os.path.join(folder, f)
        insert_spider_data.begin(artist)
        log.info(f'artist: 【{artist.name}】的本地作品全部上传完成')


# 测试
def test():
    print(Config.dispense_index(52000, 'admin'))


if __name__ == '__main__':
    scan()
