# AkShare Proxy Patch
针对 AkShare 和 efinance 的底层补丁，自动为东财接口注入代理认证头，从而避免`akshare: stock_zh_a_spot_em`、`efinance: get_realtime_quotes` 等东财 eastmoney 接口报错问题。

## 安装

1. 将官方 [akshare](https://github.com/akfamily/akshare) 或 [efinance](https://github.com/Micro-sheep/efinance) 升级到最新

```
# akshare 用户
pip install upgrade akshare

# efinance 用户
pip install upgrade efinance
```

2. 安装最新版本的 `akshare-proxy-patch`
```
pip install akshare-proxy-patch==0.2.5
```

最好默认用国外源，国内源不是最新的，版本必须 >=0.2.4

## 使用方法

1. `akshare` 和 `efinance` 使用方式一致，在文件顶部添加如下代码
```
# 文件顶部添加
import akshare_proxy_patch

# 参数1: AUTH_IP
# 参数2: AUTH_TOKEN
akshare_proxy_patch.install_patch("101.201.173.125", "")

# 你的正常业务代码不变

# 假如使用akshare
# import akshare as ak
# df = ak.stock_zh_a_spot_em()

# 假如使用 efinance
import efinance as ef
ef.stock.get_realtime_quotes()
```

## 目前Hook的接口域名清单 
- fund.eastmoney.com
- push2.eastmoney.com
- push2his.eastmoney.com

## 使用问题交流群

如遇到部分接口报错，可进群交流：

![8jmzvNOjKWFzwNUDW0Xiytcpfr50uMr5.webp](https://cdn.nodeimage.com/i/8jmzvNOjKWFzwNUDW0Xiytcpfr50uMr5.webp)