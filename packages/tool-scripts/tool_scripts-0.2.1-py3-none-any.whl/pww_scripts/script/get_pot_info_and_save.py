from pww_scripts.utils import get_resp_soup


def get_pot_info(artist: str, title: str):
    web = ''
    url = f'{web}'

    soup = get_resp_soup(url=url)
    