# AkShare Proxy Patch

> 针对 [akshare](https://github.com/akfamily/akshare)、[efinance](https://github.com/Micro-sheep/efinance)、[yfinance](https://github.com/ranaroussi/yfinance) 的🐒插件补丁，自动为函数注入请求头，解决 `stock_zh_a_spot_em`、`stock_zh_a_hist`、`get_realtime_quotes` 等接口报错问题和 Yahoo `YFRateLimitError` 问题。

## ✨ 特性

- 解决 `akshare` 接口报错问题
- 解决 `efinance` 接口报错问题
- 解决 `yfinance` Yahoo接口报错问题

## 📦 安装

1. 安装并升级官方 [akshare](https://github.com/akfamily/akshare) 或 [efinance](https://github.com/Micro-sheep/efinance) 包

2. 安装 `akshare-proxy-patch` 插件

```
pip install akshare-proxy-patch==0.3.0
```

## 🚀 使用方法（akshare / efinance / yfinance）

1. [点击前往插件官网](https://ak.cheapproxy.net/dashboard/akshare) 获取 `TOKEN`。

2. `akshare` 或 `efinance` 用户：在 Python 文件顶部添加如下代码，并替换 `你的TOKEN`。

```
# python 文件顶部添加如下代码
import akshare_proxy_patch

akshare_proxy_patch.install_patch(
    "101.201.173.125",
    auth_token="你的TOKEN",
    retry=30,
    # 封控的域名列表，可自行调整
    hook_domains=[
      "fund.eastmoney.com",
      "push2.eastmoney.com",
      "push2his.eastmoney.com",
      "emweb.securities.eastmoney.com",
    ],
)

# --------------------------
# 后续你的正常业务代码保持不变
# --------------------------

# 假如你使用 akshare
import akshare as ak
df = ak.stock_zh_a_spot_em()

# 假如你使用 efinance
import efinance as ef
ef.stock.get_realtime_quotes()
```

3. `yfinance` 用户：在 Python 文件顶部添加如下代码，并替换 `你的TOKEN`。

```
# python 文件顶部添加如下代码
import akshare_proxy_patch

akshare_proxy_patch.install_yfinance_patch(
    "101.201.173.125",
    auth_token="你的TOKEN",
    retry=30,
)

# --------------------------
# 后续你的正常业务代码保持不变
# --------------------------

import yfinance as yf

data = yf.download("AAPL", start="2017-01-01", end="2017-04-30")
```

## 📖 install_patch 参数说明

- 参数1：网关
  - 默认为 `101.201.173.125` 不可修改
- 参数2：TOKEN
  - 授权凭证
- 参数3：重试次数
  - 默认为30，建议保持不变
- 参数4：封控的域名列表
  - 接口 `URL` 包含数组中的其中一条，就会走插件。
  - 可点击 `ak` 或 `ef` 函数查看接口源码对应的 `URL`，根据封控情况细化可以降低积分消耗。
  - 如只封控 `stock_zh_a_spot_em` 这个接口，`hook_domains` 可设置为 `["https://82.push2.eastmoney.com/api/qt/clist/get"]`。

## 🛠️ 如何在 aktools 内集成插件？

`aktools` 想要集成插件，需要新建一个 `akt.py` 替换官方的 `python -m aktools` 启动命令，下面是 `akt.py` 内容：

```
# 添加插件
import akshare_proxy_patch

akshare_proxy_patch.install_patch(
    "101.201.173.125",
    auth_token="你的TOKEN",
    retry=30,
    # 封控的域名列表，可自行调整
    hook_domains=[
      "fund.eastmoney.com",
      "push2.eastmoney.com",
      "push2his.eastmoney.com",
      "emweb.securities.eastmoney.com",
    ],
)

# 启动 aktools
import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        "aktools.main:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
        # 根据 CPU 核心数调整，推荐 2×核心数 + 1
        workers=4,
        log_level="info"
    )
```

然后执行 `python akt.py` 即可启动一个 `http://127.0.0.1:8080/` 服务。只是启动方式不同而已，使用请参考 [aktools 官方文档](https://github.com/akfamily/aktools)。

## ❓ 我没使用 akshare 或 efinance，能集成插件吗？

- 如果使用 Python 语言的 `requests` 库请求接口，插件能自动 hook 住请求，正常工作。
- 如果您使用其他语言或 python 的其他库，可 [手动提取代理](http://101.201.173.125:47001/api/akshare-auth?token=&version=0.2.13) 自行实现封控解除。

## 💬 使用问题交流群

如使用时遇到问题，或对插件有什么意见或建议，可进群交流：

![YpRjixvpykLmzPtrX0kIkdPlvffOFJvF.webp](https://cdn.nodeimage.com/i/YpRjixvpykLmzPtrX0kIkdPlvffOFJvF.webp)
