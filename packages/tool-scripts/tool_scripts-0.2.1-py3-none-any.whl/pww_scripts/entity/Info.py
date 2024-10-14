import datetime
import decimal
from dataclasses import dataclass


@dataclass
class Info:
    # 番号
    number: str

    # 原始标题
    origin_title: str

    # 汉化标题
    chinese_title: str

    # 简介
    desc: str

    # 剧情
    story: str

    # 艺术家
    actress: str

    # 出版日期
    published: datetime.date

    # 文件大小（GB）
    size: decimal

    # 时长
    duration: datetime.timedelta

    # 厂商
    manufacturer: str

    # 文件夹地址
    path: str

    # 是否有效
    is_valid: bool

    def __init__(self, _number='', _origin_title='', _chinese_title='', _desc='', _story='', _actress='',
                 _published=datetime.date(1, 1, 1), _size='0GB', _duration=datetime.timedelta(0),
                 _manufacturer='',_path=''):
        self.number = _number
        self.origin_title = _origin_title
        self.chinese_title = _chinese_title
        self.desc = _desc
        self.story = _story
        self.actress = _actress
        self.published = _published
        self.size = _size
        self.duration = _duration
        self.manufacturer = _manufacturer
        self.path = _path
        self.is_valid = False
