from dataclasses import dataclass


@dataclass
class Pot:
    """
    - 每一期作品
    """

    # ID
    id = 0
    # 作者ID
    artist_id = 0
    # 标题
    title = ''
    # 简介
    introduction = ''
    # 预览图地址
    preview = ''
    # 出版日期
    published = ''
    # 文件类型
    type = ''
    # 文件地址
    path = ''
    # 时长 页数
    length = ''
    # 存储大小
    size = ''
    # 是否已经下载
    is_download = 1

    def transform(self, pot_params):
        self.title = pot_params.title
        self.published = pot_params.published
        self.path = pot_params.pot_file_path
