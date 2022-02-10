import requests, os, sys
from bs4 import BeautifulSoup
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("graber")



# url - 下载地址
# name - 文件名
# path - 保存路径
def download_the_img(url, name, path):
    rsp=requests.get(url)
    abs_file = path + '/' + name
    log.info('保存图片：{}'.format(abs_file))
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
            response_cur = requests.get(url)
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


# log.info("接受到{}个参数, 参数列表: {}".format(len(sys.argv), str(sys.argv)))

if len(sys.argv) == 3:
    size = sys.argv[1]
    dir = sys.argv[2]
    size_list = ['2560x1440', '1600x900', '2560x1600', '1920x1200', '1680x1050', '1440x900', '1280x800']
    if size not in size_list:
        log.error('指定的图片大小不存在, 请总下列大小中选择! \r\n {}'.format(str(size_list)))
    elif not os.path.isdir(dir):
        log.error('请输入正确的保存路径!')
    else:
        response = requests.get('https://erowall.com/')
        max_page = get_the_max_page_number(response.content)
        download_each_page(response.content, size, dir)

        for cur in range(2, max_page):
            cur_rsp = requests.get('https://erowall.com/dat/page/'+str(cur))
            download_each_page(cur_rsp.content, size, dir)           
else:
    log.info("请指定图片大小和保存路径, 比如: graber 2560x1440 D:/temp")    
