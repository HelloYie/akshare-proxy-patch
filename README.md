# AkShare Proxy Patch
针对 AkShare 的底层补丁，自动为东财等接口注入代理认证头，从而避免 `stock_zh_a_spot_em` 等方法报错。

## 安装

```
pip install --upgrade akshare-proxy-patch
```

## 使用

1. 登录 https://cheapproxy.net，获取授权码 `AUTH_IP` 和 `AUTH_TOKEN`

2. 将 akshare 升级到最新

```
pip install --upgrade akshare
```

3. 在使用 akshare 文件顶部添加下面的内容 
```
# 文件顶部添加
import akshare_proxy_patch

akshare_proxy_patch.install_patch("AUTH_IP", "AUTH_TOKEN")

# 你的正常业务代码......
# import akshare as ak
# df = ak.stock_zh_a_spot_em()
```

## 目前Hook的接口域名清单 
- fund.eastmoney.com
- push2.eastmoney.com
- push2his.eastmoney.com

## TODO 
- 多线程情况下容易出现问题，需暂时不使用多线程或减少线程数

## 使用问题交流群

![8jmzvNOjKWFzwNUDW0Xiytcpfr50uMr5.webp](https://cdn.nodeimage.com/i/8jmzvNOjKWFzwNUDW0Xiytcpfr50uMr5.webp)