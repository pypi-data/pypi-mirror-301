from dataclasses import fields

from mysql.connector import pooling
from mysql.connector.pooling import MySQLConnectionPool

from pww_scripts.entity.Artist import Artist


class MySQLConnection:
    """
    - mysql数据库操作类
    """
    drive: str
    database: str
    connection_pool: MySQLConnectionPool

    def __init__(self, _drive='localhost', _database=''):
        self.drive = _drive
        self.database = _database

        # 创建连接池
        if self.drive == 'aliyun':
            dbconfig = {
                "database": _database,
                "user": "root",
                "password": "123456",
                "host": "114.55.119.85",
                'port': '3306'
            }
        else:
            dbconfig = {
                "database": _database,
                "user": "root",
                "password": "123456",
                "host": "127.0.0.1",
                'port': '3306'
            }
        pool_name = "mypool"
        pool_size = 10

        self.connection_pool = pooling.MySQLConnectionPool(pool_name=pool_name,
                                                           pool_size=pool_size,
                                                           **dbconfig)

    @staticmethod
    def get_field(entity, columns=None, values=None) -> None:
        """
        - 获取实体的列名和值
        """
        for field in fields(entity):
            if field.name == 'is_valid': continue
            if field.name == 'id': continue
            columns.append(field.name)
            values.append(getattr(entity, field.name))

    def __get_connection(self):
        return self.connection_pool.get_connection()

    def insert_pot(self, pot) -> int:
        """
        - 将数据插入mysql
        """
        conn = self.__get_connection()
        cursor = conn.cursor()
        values = []
        values.append(pot.id)
        values.append(pot.artist_id)
        values.append(pot.title)
        values.append(pot.introduction)
        values.append(pot.preview)
        values.append(pot.published)
        values.append(pot.type)
        values.append(pot.path)
        values.append(pot.length)
        values.append(pot.size)
        values.append(pot.is_download)

        # 构建完整的 SQL 查询
        query = (f'INSERT INTO pot (id, artist_id,title, introduction, preview, published, type, path, length, size, is_download)'
                 f' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        cursor.execute(query, values)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id

    def select_artist(self, name):
        conn = self.__get_connection()
        cursor = conn.cursor()
        qurry = f'SELECT * FROM artist WHERE name=%s'
        cursor.execute(qurry, (name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def insert_artist(self, artist: Artist):
        """
        - 插入作者 并返回ID
        """
        conn = self.__get_connection()
        cursor = conn.cursor()
        qurry = f'INSERT INTO artist (name, local_path) VALUES (%s, %s)'
        cursor.execute(qurry, (artist.name, artist.local_path))
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.lastrowid

    def update_artist_pot_index(self, artist):
        """
        - 更新作者的作品索引
        """
        artist.pot_index += 1
        conn = self.__get_connection()
        cursor = conn.cursor()
        qurry = f'UPDATE artist set pot_index=%s WHERE name=%s'
        cursor.execute(qurry, (artist.pot_index, artist.name))
        conn.commit()
        cursor.close()
        conn.close()

    def select_pot(self, pot):
        conn = self.__get_connection()
        cursor = conn.cursor()
        qurry = f'SELECT * FROM pot WHERE path=%s'
        cursor.execute(qurry, (pot.path,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
