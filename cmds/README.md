# 安装  
由于开发环境并不属于python的包路径，而且我们的click入口需要引用自己项目中的其他逻辑，所以在安装时需要添加额外包路径。  
官方说明文档：[Using Spec Files](https://pyinstaller.readthedocs.io/en/stable/spec-files.html)  
命令举例  
``` Python  
pyinstaller --paths '/your/direction/path/bllools-spider' -F graber_cmd.py
```  

这时，pyinstaller运行时，首先会生成```.spec```文件， 文件中添加了pathx路径:  
```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['graber_cmd.py'],
             pathex=["'/your/direction/path/bllools-spider'"],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
...

```  

最终，在安装的日志中也能看到识别出包地址的改变：  
```
...   
320 INFO: checking Analysis
337 INFO: Building because pathex changed        
337 INFO: Initializing module dependency graph...
...
```
