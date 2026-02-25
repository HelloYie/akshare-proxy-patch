# AkShare Proxy Patch

针对 akshare 和 efinance 的插件补丁，自动为东财接口注入代理认证头，从而避免`akshare: stock_zh_a_spot_em`、`efinance: get_realtime_quotes` 等东财 eastmoney 接口报错问题。

## 安装

1. 将官方 [akshare](https://github.com/akfamily/akshare) 或 [efinance](https://github.com/Micro-sheep/efinance) 升级到最新

```
# akshare 用户
pip install --upgrade akshare

# efinance 用户
pip install --upgrade efinance
```

2. 安装最新版本的 `akshare-proxy-patch`

```
pip install akshare-proxy-patch==0.2.7
```

## 使用方法

`akshare` 和 `efinance` 使用方式一致，在文件顶部添加2行代码即可，无需寻找代理IP和其他额外操作。

```
# 文件顶部添加2行代码
import akshare_proxy_patch

akshare_proxy_patch.install_patch("101.201.173.125", "", 30)


# 后续你的正常业务代码保持不变

# 假如你使用akshare
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
  - 默认为空，每天可免费使用一定次数。如有更多需求，可[点击此处注册](https://cheapproxy.net/)并申请 正式的`AUTH_TOKEN`。
- 参数3：重试次数
  - 默认为30，建议保持不变

## 目前 Hook 的接口域名清单

- fund.eastmoney.com
- push2.eastmoney.com
- push2his.eastmoney.com

## 使用问题交流群

如遇到部分接口报错，或有什么意见或建议，可进群交流：

![cBdTtCUyUMu90DljeIpzLFD5IFqPmW9y.webp](https://cdn.nodeimage.com/i/cBdTtCUyUMu90DljeIpzLFD5IFqPmW9y.webp)
