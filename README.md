
使用`deploy.py`脚本完成RBDSR的安装、卸载等想过操作

# 安装

`python deploy.py install`

# 卸载

`python deploy.py uninstall`

RBDSR卸载后，会有后缀为`-orig`的备份文件残留，该文件不影响用户使用，若想清除可以使用`clean`参数，eg: `python deploy.py clean`

# 查询是否安装RBDSR

`python deploy.py check`


# Thanks
本程序在[mstarikov/rbdsr](https://github.com/mstarikov/rbdsr)的基础上修改、适配而成。感谢 Mark Starikov 对RBDSR的共享。

