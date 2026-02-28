# AkShare Proxy Patch

针对 `akshare` 和 `efinance` 的插件补丁，自动为东财接口注入请求头，从而避免`stock_zh_a_spot_em`、`get_realtime_quotes` 等东财 eastmoney 接口报错问题。

## 安装

1. 安装好官方 [akshare](https://github.com/akfamily/akshare) 或 [efinance](https://github.com/Micro-sheep/efinance) 包

2. 安装 `akshare-proxy-patch` 插件

```
pip install akshare-proxy-patch==0.2.8
```

## 使用方法

`akshare` 和 `efinance` 使用方式一致，在文件顶部添加2行代码即可，无需其他额外操作。

```
# python 文件顶部添加2行代码
import akshare_proxy_patch

akshare_proxy_patch.install_patch("101.201.173.125", "", 30)


# 后续你的正常业务代码保持不变

# 假如你使用 akshare
import akshare as ak
df = ak.stock_zh_a_spot_em()

# 假如你使用 efinance
import efinance as ef
ef.stock.get_realtime_quotes()
```

## install_patch 参数说明

- 参数1：网关
  - 默认为 `101.201.173.125` 不可修改
- 参数2：AUTH_TOKEN
  - 默认为空，每天可免费使用一定次数。如有更多需求，可[点击此处注册](https://ak.cheapproxy.net/dashboard/akshare)申请正式的 `AUTH_TOKEN`。
- 参数3：重试次数
  - 默认为30，建议保持不变

## 目前 Hook 的接口域名清单

- fund.eastmoney.com
- push2.eastmoney.com
- push2his.eastmoney.com

## 我是手动爬取的东财接口，能用插件吗？

能。如果您没有使用 `akshare` 或 `efinance`，而是手动调用的东财接口，只要代码是使用的 `requests`，插件都能 hook 住请求，正常工作。

## 使用问题交流群

如使用时遇到问题，或对插件有什么意见或建议，可进群交流：

![7sEblPiT7tEdCPrA3nEyekVYxsMZDDgy.webp](https://cdn.nodeimage.com/i/7sEblPiT7tEdCPrA3nEyekVYxsMZDDgy.webp)
