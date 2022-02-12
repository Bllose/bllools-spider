# import sys
# from os.path import abspath, join, dirname
# sys.path.insert(0, join(abspath(dirname(__file__)), '..'))
# print(sys.path)

import click
# from common import func
# from pics.erowall import graber


import requests, os, sys
from requests.models import Response
from bs4 import BeautifulSoup
import logging
from typing import Tuple
from urllib3.exceptions import IncompleteRead, ProtocolError, MaxRetryError
from requests.exceptions import ChunkedEncodingError, SSLError, ConnectionError
from ssl import SSLEOFError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("graber")

size_list = ['2560x1440', '1600x900', '2560x1600', '1920x1200', '1680x1050', '1440x900', '1280x800']
proxy = {
        'http':'127.0.0.1:63571',
        'https':'127.0.0.1:63571'
        }

use_proxy = False

def set_proxy(host, port=None) -> None:
    if port:
        proxy['http'] = host + ':' + port
        proxy['https'] = host + ':' + port
    else:
        proxy['http'] = host
        proxy['https'] = host

def GET(url) -> Response:
    if use_proxy:
        return requests.get(url, proxies=proxy)
    else:
        return requests.get(url)

# url - 下载地址
# name - 文件名
# path - 保存路径
def download_the_img(url, name, path):
    try:
        rsp=GET(url)
    except (IncompleteRead, ProtocolError, ChunkedEncodingError) as e:
        try:
            rsp=GET(url)
        except (IncompleteRead, ProtocolError, ChunkedEncodingError) as e:
            log.error('尝试下载文件{}时出现异常,跳过当前文件, 报错信息:\r\n{}'.format(name, str(e)))
            return
    abs_file = path + '/' + name
    log.info('保存图片: {}'.format(abs_file))
    with open(abs_file, 'wb') as f:
            f.write(rsp.content)


def get_file_name(path) -> Tuple[str, str]:
    import re
    regex=r'/d/([0-9]+)/([^/]+)/'
    matcher = re.match(regex, path)
    if matcher:
        return matcher.group(1),matcher.group(2)
    else:
        return None, None


def already_download(path, name) -> bool:
    import os
    for root, dirs, files in os.walk(path):
        return name in files

# 传递一个页面，并下载该页面中指定大小的图片
def download_each_page(html_content, size, dir):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    counter = 0
    # 获取前页面的所有图片初始地址
    for link in soup.find_all('a'):
        path = link.get('href')
        if path.startswith('/w/'):
            counter += 1
            log.info('尝试下载第{}张图片: {}'.format(counter, path))
            url = 'https://erowall.com' + path
            # print(url) # https://erowall.com/w/33954/                     
            response_cur = GET(url)           
            soup_cur = BeautifulSoup(response_cur.text, 'html.parser')
            for link_cur in soup_cur.find_all('a'):
                path_cur = link_cur.get('href')
                name, size_cur = get_file_name(path_cur)
                if name and size_cur and size_cur == size:
                    download_url = r'https://erowall.com/download_img.php?dimg=' + name + r'&raz=' + size_cur
                    saved_path = dir
                    file_name = name+'_'+size+'.png'
                    if already_download(saved_path, file_name):
                        log.warning('{} 文件已经存在,跳过该文件!'.format(file_name))
                    else:
                        download_the_img(download_url, name+'_'+size+'.png', saved_path)
                    continue
                    # print(url_cur)
                    # https://erowall.com/d/33944/2560x1440/
                    # https://erowall.com/download_img.php?dimg=33954&raz=2560x1440


def get_the_max_page_number(html_content) -> int:
    import re
    soup = BeautifulSoup(html_content, 'html.parser')
    regex = r'/dat/page/([0-9]+)'
    max_page = 0
    for link in soup.find_all('a'):
        path = link.get('href')
        matcher = re.match(regex, path)
        if matcher:
            cur_page = int(matcher.group(1))
            if max_page < cur_page:
                max_page = cur_page
    return max_page


def main_entry(size, dir, proxy, cur_page = 1):
    if size not in size_list:
        log.error('指定的图片大小不存在, 请总下列大小中选择! \r\n {}'.format(str(size_list)))
    elif not os.path.isdir(dir):
        log.error('请输入正确的保存路径!')
    else:
        if proxy.strip():
            global use_proxy
            use_proxy = True
            set_proxy(proxy)
            log.info("使用代理{}".format(proxy))

        try:
            response = GET('https://erowall.com/')
            max_page = get_the_max_page_number(response.content)
            log.info("即将开始下载,将保存到路径:{}".format(dir))
            if cur_page > 1:
                for cur in range(cur_page, max_page):
                    cur_rsp = GET('https://erowall.com/dat/page/'+str(cur))
                    log.info("开始第{}页下载".format(cur))
                    download_each_page(cur_rsp.content, size, dir)
            else:
                download_each_page(response.content, size, dir)
                for cur in range(2, max_page):
                    log.info("开始第{}页下载".format(cur))
                    cur_rsp = GET('https://erowall.com/dat/page/'+str(cur))
                    download_each_page(cur_rsp.content, size, dir)   
        except (IncompleteRead, ChunkedEncodingError) as e:
            log.error("请求异常结束!")
        except (MaxRetryError, SSLError, SSLEOFError) as e:
            log.error("不支持代理,请关闭代理后重试.")
        except (ConnectionError, ProtocolError) as e:
            log.error("网络不通, 需要科学上网")
       


@click.group()
def cli() -> None:
    pass


@click.command("erowall", short_help="爬它的壁纸")
# @click.option('--level', default='INFO', help='过程中日志级别, 默认是 INFO')
@click.option('--size', default='2560x1440', help='下载壁纸大小')
@click.option('--dir', default='/temp', help='下载后保存路径')
@click.option('--proxy', default = '', help='使用的代理地址')
@click.option('--cur', default=1, help='从第几页开始下载')
def spiter_erowall_wallpaper(size, dir, proxy, cur):
    # logLevel = func.getLevel(level)
    main_entry(size, dir, proxy, cur_page=cur)


cli.add_command(spiter_erowall_wallpaper)

if __name__ == '__main__':
    spiter_erowall_wallpaper()
