# bllools-spider
我的爬虫们~  
- [graber](https://github.com/Bllose/bllools-spider/raw/main/pics/erowall/dist/graber.exe)
- [graber_cmd](https://github.com/Bllose/bllools-spider/raw/main/cmds/dist/graber_cmd.exe)
## graber_cmd  
使用 ```help``` 查看使用信息:  
``` 
>graber_cmd --help
Usage: graber_cmd [OPTIONS]

Options:
  --level TEXT   过程中日志级别, 默认是 INFO
  --size TEXT    下载壁纸大小
  --dir TEXT     下载后保存路径
  --proxy TEXT   使用的代理地址
  --cur INTEGER  从第几页开始下载
  --help         Show this message and exit.
```  

目前还不支持直接走系统的代理， 如果需要翻墙才能下载， 那么需要指定代理的使用。  
否则会报错:  
```
>graber_cmd
ERROR:graber:不支持操作系统默认代理,请通过 --proxy 你的代理地址 正确使用代理功能
```

在window10中，打开“代理”或者“更改代理设置” 设置页面，就能看到【使用代理服务器】栏位， 下面有具体代理地址和端口。  
![proxy_example](https://github.com/Bllose/bllools-spider/blob/main/sources/proxy_example.png)  
然后将这个地址写入代理参数```--proxy```即可。  
比如:  
```
>graber_cmd --proxy 127.0.0.1:63571
INFO:graber:使用代理127.0.0.1:63571
INFO:graber:即将开始下载,将保存到路径:/temp
INFO:graber:尝试下载第1张图片: /w/33954/
```
