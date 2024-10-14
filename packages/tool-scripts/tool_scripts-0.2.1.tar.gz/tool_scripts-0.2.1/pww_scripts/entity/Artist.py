from dataclasses import dataclass


@dataclass
class Artist:
    """
    - 作者实体
    """

    # 作者ID
    id = 0
    # 作者名称
    name = ''
    # 链接
    link = ''
    # 本地地址
    local_path = ''
    # 最后收集时间
    last_collected = ''
    # 最后更新时间
    last_updated = ''
    # 作品索引
    pot_index = 0

    def transform(self, db_data):
        self.id = db_data[0]
        self.name = db_data[1]
        self.link = db_data[2]
        self.local_path = db_data[3]
        self.last_collected = db_data[4]
        self.last_updated = db_data[5]
        self.pot_index = db_data[6]



