import configparser
import datetime
import os
import re

import requests
from PIL import Image
import cv2
from bs4 import BeautifulSoup

from moviepy.video.io.VideoFileClip import VideoFileClip

from pww_scripts.init.parameter import PROXY, HEADER
from pww_scripts.entity.Log import log


def get_resp_soup(url) -> BeautifulSoup:
    """
    - 获取响应体
    :param url: 请求网址
    :return: BeautifulSoup
    """
    response = requests.get(url=url, proxies=PROXY, headers=HEADER)
    soup = BeautifulSoup(response.text, 'html.parser')
    response.close()
    return soup


def get_response(url):
    return requests.get(url=url, headers=HEADER, proxies=PROXY, stream=True)


def getcwd(path) -> str:
    """
    - 获取父级路径
    :param path: 字符串路径
    :return: str
    """
    return path.rsplit('\\', 1)[0]


def get_suffix(string: str):
    return string.split('.')[1]


def getfn(path) -> str:
    """
    - 通过路径获取最后一层的文件夹名称
    """
    return path.rsplit('\\', 1)[1]


def is_equal(path, size):
    """
    - 判断文件是否重复
    """
    print(f'{os.path.getsize(path)}   {size}')
    return os.path.getsize(path) == size


def get_filesize(path, unit='GB') -> str:
    """
    - 获取文件大小
    """
    if unit == 'GB':
        return format(os.path.getsize(path) / 1024 / 1024 / 1024, '.2f') + 'GB'
    elif unit == 'MB':
        return format(os.path.getsize(path) / 1024 / 1024, '.2f') + 'MB'
    elif unit == 'KB':
        return format(os.path.getsize(path) / 1024, '.2f') + 'KB'
    else:
        return str(os.path.getsize(path)) + 'byte'


def get_strnumber_bytesize(strnumber: str) -> int:
    """
    - 获取字符大小的字节数值
    """
    if 'byte' in strnumber: return int(strnumber[:-4])
    if 'kb' in strnumber.lower(): return int(float(strnumber[:-2]) * 1000)
    if 'mb' in strnumber.lower(): return int(float(strnumber[:-2]) * 1000 * 1000)
    if 'gb' in strnumber.lower(): return int(float(strnumber[:-2]) * 1000 * 1000 * 1000)


def size_add(first: str, second: str, return_unit='KB') -> str:
    """
    - 两个字符串类型的文件大小相加
    """
    first_count = get_strnumber_bytesize(first)
    second_count = get_strnumber_bytesize(second)
    if return_unit == 'GB':
        return str((first_count + second_count) / 1000 / 1000 / 1000) + 'GB'
    if return_unit == 'MB':
        return str((first_count + second_count) / 1000 / 1000) + 'MB'
    if return_unit == 'KB':
        return str((first_count + second_count) / 1000) + 'KB'
    else:
        return str(first_count + second_count) + 'byte'


def get_movie_duration(path) -> datetime.timedelta:
    """
    - 获取视频时长
    """
    with VideoFileClip(path) as video:
        return datetime.timedelta(seconds=int(video.duration))


def upload_error(filename, exception):
    log.info(f'文件夹【{filename}】备案失败 错误信息: {exception}')


def upload_success(filename):
    log.info(f'文件夹【{filename}】备案成功')


def self_error(tip, exception):
    """
    - 自定义系统错误
    """
    log.info(f'{tip} 错误信息: {exception}')


def replace_not_invalid_string(string):
    """
    - 替换掉文件夹不允许出现的字符
    """
    return re.sub(r'[\\/:*?"<>|]', ' ', string)


def get_resolution(file) -> int:
    """
    - 获取文件清晰度
    """
    suffix = file.split('.')[1]
    if suffix == 'mp4':
        video = cv2.VideoCapture(file)
        w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    else:
        img = Image.open(file)
        w, h = img.size
    return int(f'{w}px*{h}px')


def get_folder_size(folder_path):
    """
    - 获取文件夹的大小
    """
    total_size = 0
    # 遍历文件夹中的所有文件和子文件夹
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # 累加文件大小
            total_size += os.path.getsize(file_path)
    return total_size



class Config:

    @staticmethod
    def get_pot_index() -> int:
        """
        - 从本地配置文件获取作品ID的索引
        """
        tc = configparser.ConfigParser()
        tc.read('init\\config.ini', encoding='utf-8')
        return int(tc.items('MySQL')[0][1])

    @staticmethod
    def save_pot_index(index) -> bool:
        """
        - 保存作品索引到本地配置文件
        """
        config_path = 'init\\config.ini'
        c = configparser.ConfigParser()
        c.read(config_path, encoding='utf-8')
        try:
            c.set('MySQL', 'pot_id_index', str(index))
            with open(config_path, 'w', encoding='utf-8') as cfg:
                c.write(cfg)
            log.info(f'索引【{index}】保存成功')
            return True
        except Exception as e:
            log.info(f'索引【{index}】保存失败 失败信息: {e}')
            return False

    @staticmethod
    def dispense_index(artist_id, artist_name) -> int:
        """
        - 分配作者的作品起始索引 并存入本地配置文件
        """
        index = int(f'768{artist_id}00000')
        config_path = 'init\\config.ini'
        c = configparser.ConfigParser()
        c.read(config_path, encoding='utf-8')
        try:
            c.set('Artist', artist_name, str(index))
            log.info(f'分配作者【{artist_name}】的索引成功')
            with open(config_path, 'w', encoding='utf-8') as cfg:
                c.write(cfg)
            return index
        except Exception as e:
            log.error(f'分配作者【{artist_name}】的索引失败 错误信息: {e}')


class Resolution:
    HD = 1080
    FHD = 1920
    QHD = 2560
    UHD = 3840

    @staticmethod
    def get_resolution_name(number):
        """
        - 通过清晰度获取对应的名称
        """
        if number == 1080: return 'HD'
        if number == 1920: return 'FHD'
        if number == 2560: return '2K'
        if number == 3840: return '4K'
        else: return 'UKN'