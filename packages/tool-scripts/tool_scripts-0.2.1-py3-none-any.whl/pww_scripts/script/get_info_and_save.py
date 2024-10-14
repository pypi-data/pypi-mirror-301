from pww_scripts.init.parameter import *
from pww_scripts.entity.Backtrack import Backtrack
from pww_scripts.entity.Info import Info
from pww_scripts.entity.MySQLConnection import MySQLConnection
from pww_scripts.utils import *


def __get_info(info: Info) -> bool:
    """
    - 通过番号获取信息
    :param info: 信息类 -> number
    :return: boolean
    """

    # 1、带参请求
    url = f'{LIBRARY1}/search?type=id&q={info.number}'
    soup = get_resp_soup(url=url)

    # 2、筛选出结果
    result = soup.select_one('div[class="works"]')

    # 3、获取信息
    if result:
        url = LIBRARY1 + result.select_one('a[class="work"]')['href']
        soup = get_resp_soup(url)
        info.actress = soup.select_one('.actress').text
        info.chinese_title = replace_not_invalid_string(soup.select_one('h1').text)
        info.desc = soup.select_one('p[class="contents"]').text

        attributes = soup.select_one('div[class="attributes"]').select_one('dl')
        for line in str(attributes).splitlines():
            if '番号' in line and '番号前缀' not in line:
                info.number = re.findall('(?<=<dt>).*?(?=</dt>)', line)[0]
            elif '发行时间' in line:
                info.published = re.findall('(?<=<dt>).*?(?=</dt>)', line)[0]
            elif '片商' in line:
                temp = re.findall('(?<=<dt>).*?(?=</dt>)', line)[0]
                info.manufacturer = re.findall('(?<=">).*?(?=</a>)', temp)[0]

            elif '类别' in line:
                break
        return True
    else:
        return False


def __get_media_image(info: Info) -> None:
    """
    - 获取图片资源
    """
    url = f''
    soup = get_resp_soup(url=url)
    result = soup.select_one('div[class="works"]')
    if result:
        url = LIBRARY1 + result.select_one('a[class="work"]')['href']
        soup = get_resp_soup(url)
        images = soup.select('')
        count = 1
        for image in images:
            content = get_response(image)
            path = f'{info.path}\\{str(count).rjust(3, "0")}.{get_suffix(image)}'
            # 如果文件存在且相同 则跳过
            if os.path.exists(path) and is_equal(path, content.headers.get('content-type')):
                continue
            with (open(path, 'ab')) as f:
                for chunk in content.iter_content(chunk_size=1024):
                    f.write(chunk)
                    f.flush()
                content.close()


def save_info(info: Info) -> bool:
    """
    - 保存信息到数据库
    - 原子化操作
    :param info: Info
    :return: boolean
    """

    # 文件夹名称
    fn = getfn(info.path)

    # 如果番名为空 则抛出异常
    if info.number is None:
        upload_error(fn, f'[Error]: 该文件夹未提取到番号: {info.number}')
        return False

    # 连接数据库
    sql = MySQLConnection('jtm')

    # 判断该文件夹是否已经备案
    result = sql.select_title(fn)
    if len(result) > 0:
        upload_error(fn, '[Info] 该文件夹已经备案')
        return False

    # 获取图片资源
    __get_media_image(info)

    # 判断 info 是否有效 无效则通过番名进行内部获取
    if not info.is_valid:
        __get_info(info)

    # 简易番号
    simple_number = info.number.replace(re.findall(r'\(.*\)', info.number)[0], '').strip()

    # 回溯器
    backtrack = Backtrack(_old=[], _new=[], _folder=[])

    # 修改文件夹名称
    if simple_number.lower() not in info.chinese_title.lower():
        backtrack.add_new(f'{getcwd(info.path)}\\{info.number}-{info.chinese_title}')
    else:
        backtrack.add_new(f'{getcwd(info.path)}\\{info.chinese_title}')
    backtrack.add_old(info.path)

    os.rename(backtrack.old[-1], backtrack.new[-1])

    # 新的文件夹路径
    folder = backtrack.new[-1]
    info.path = folder

    # 修改视频名称 获取视频大小 时长
    movie_list = os.listdir(folder)
    for movie in movie_list:
        if '.jpg' in movie: movie_list.remove(movie)
    if len(movie_list) == 1:
        fp = f'{folder}\\{movie_list[0]}'

        info.size = get_filesize(fp)
        info.duration = get_movie_duration(fp)

        suffix = movie_list[0].split('.')[1]

        backtrack.add_old(fp)
        backtrack.add_new(f'{folder}\\{simple_number}.{suffix}')
        try:
            os.rename(backtrack.old[-1], backtrack.new[-1])
        except Exception as e:
            upload_error(fn, e)
            backtrack.rename_backtrack()
    else:
        i = 1
        for movie in movie_list:
            fp = f'{folder}\\{movie}'

            info.size = size_add(info.size, get_filesize(fp), 'GB')
            info.duration += get_movie_duration(fp)

            suffix = movie.split('.')[1]
            backtrack.add_old(f'{folder}\\{movie}')
            backtrack.add_new(f'{folder}\\{simple_number}-{i}.{suffix}')
            i += 1
            try:
                os.rename(backtrack.old[-1], backtrack.new[-1])
            except Exception as e:
                upload_error(fn, e)
                backtrack.rename_backtrack()

    # 将信息存入数据库
    try:
        sql.insert_pot('info', info)
        upload_success(fn)
        return True
    except Exception as e:
        upload_error(fn, e)
        backtrack.add_new('')
        backtrack.add_old('')
        backtrack.rename_backtrack()
        return False
