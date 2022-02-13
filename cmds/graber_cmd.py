# import sys
# from os.path import abspath, join, dirname
# sys.path.insert(0, join(abspath(dirname(__file__)), '..'))
# print(sys.path)

import click
from common import func
from pics.erowall import graber

@click.group()
def cli() -> None:
    pass


@click.command("erowall", short_help="爬它的壁纸")
@click.option('--level', default='INFO', help='过程中日志级别, 默认是 INFO')
@click.option('--size', default='2560x1440', help='下载壁纸大小')
@click.option('--dir', default='/temp', help='下载后保存路径')
@click.option('--proxy', default = '', help='使用的代理地址')
@click.option('--cur', default=1, help='从第几页开始下载')
def spiter_erowall_wallpaper(size, dir, proxy, cur, level):
    logLevel = func.getLevel(level)
    graber.main_entry(size, dir, proxy, cur_page=cur)


cli.add_command(spiter_erowall_wallpaper)

if __name__ == '__main__':
    spiter_erowall_wallpaper()
