import humanize

from pww_scripts.init.parameter import IMAGE_SUFFIX
from pww_scripts.entity.Artist import Artist
from pww_scripts.entity.MySQLConnection import MySQLConnection
from pww_scripts.entity.Pot import Pot
from pww_scripts.utils import *


def get_pot_info(artist: Artist, pot: Pot):
    web = ''

    url = f'{web}/search?type=id&q={web}'
    soup = get_resp_soup(url=url)


def __split_filename(filename: str, pot: Pot):
    """
    - 通过文件名获取出版日期和标题
    """
    result = filename.split('#')
    pot.title = result[1]
    pot.published = result[0].strip()


def begin(artist: Artist):
    # 数据库建表
    sql = MySQLConnection('aliyun', 'acg')
    # 查询数据库是否存在该作者的信息
    database_artist = sql.select_artist(artist.name)
    if database_artist:
        artist.transform(database_artist)
    else:
        artist.id = sql.insert_artist(artist)
        artist.pot_index = 0
    for file in os.listdir(artist.local_path)[:-1]:
        pot = Pot()

        # **计算ID
        pot.id = f'92{artist.id}{str(artist.pot_index).rjust(4, "0")}'
        pot.artist_id = artist.id

        # **获取作品存储地址
        pot.path = os.path.join(artist.local_path, file)

        # **通过文件夹名获取 出版日期 和 标题
        __split_filename(file, pot)

        # 检查该作品是否已经上传到数据库
        if sql.select_pot(pot):
            log.warn(f'pot【{pot.published} {pot.title}】已经上传至数据库')
            continue

        pot_list = os.listdir(pot.path)
        _type = ['', '']
        _resolution = ['', '']
        _length_duration = datetime.timedelta(0, 0, 0)
        _length_page = 0
        # 统计时长和页数
        for item in pot_list:
            file_path = os.path.join(pot.path, item)
            # 如果是图片 直接跳过清晰度计算
            if item.split('.')[1] in IMAGE_SUFFIX:
                _type[0] = 'ACG'
                _length_page += 1
            else:
                _type[1] = 'VID'
                _length_duration += get_movie_duration(file_path)
        # **计算length
        if _length_duration == datetime.timedelta(0, 0, 0):
            pot.length = str(_length_page).rjust(3, "0")
        elif _length_page == 0:
            pot.length = str(_length_duration)
        else:
            pot.length = f'{_length_duration} + {str(_length_page).rjust(3, "0")}'

        # **计算作品类型
        if _type[0] == 'ACG' and _type[1] == 'VID':
            pot.type = 'ACG+VID'
        elif _type[1] == 'VID':
            pot.type = 'VID'
        elif _type[0] == 'ACG':
            pot.type = 'ACG'

        # **计算作品大小
        size_bytes = get_folder_size(pot.path)
        pot.size = str(humanize.naturalsize(size_bytes))

        # 保存到数据库
        sql.insert_pot(pot)
        log.info(f'pot【{pot.published} {pot.title}】上传成功')

        # 作者的作品索引+1
        sql.update_artist_pot_index(artist)
