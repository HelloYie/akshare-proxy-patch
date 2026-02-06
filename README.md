# AkShare Proxy Patch
针对 AkShare 的底层补丁，自动为东财等接口注入代理认证头，从而避免 `stock_zh_a_spot_em` 等方法报错。

## 安装

```
pip install akshare-proxy-patch -i https://mirrors.aliyun.com/pypi/simple
```

## 使用

1. 访问 https://cheapproxy.net 联系客服，获取授权码 `AUTH_TOKEN`

2. 在使用 akshare 文件顶部添加下面的内容 
```
import akshare_proxy_patch

akshare_proxy_patch.install_patch("AUTH_TOKEN")


# import akshare as ak
# df = ak.stock_zh_a_spot_em()
# 你的其他代码......
```
