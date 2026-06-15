# AkShare Proxy Patch

> 针对 [akshare](https://github.com/akfamily/akshare)、[efinance](https://github.com/Micro-sheep/efinance)、[yfinance](https://github.com/ranaroussi/yfinance) 的🐒插件补丁，解决 `stock_zh_a_spot_em`、`stock_zh_a_hist`、`get_realtime_quotes` 等接口报错问题和 Yahoo `YFRateLimitError` 问题。并对 `akshare` 部分接口进行多线程加速处理。

## ✨ 特性

- 解决 `akshare` 的 `stock_zh_a_spot_em`、`stock_zh_a_hist` 接口报错问题
- 解决 `efinance` 的 `get_realtime_quotes` 等接口报错问题
- 解决 `yfinance` Yahoo接口国内无法使用问题
- 多线程加速 `stock_zh_a_spot_em`、`stock_individual_fund_flow_rank` 等 `akshare` 接口

## 📦 安装

1. 安装并升级官方 [akshare](https://github.com/akfamily/akshare) 或 [efinance](https://github.com/Micro-sheep/efinance) 包

2. 安装 `akshare-proxy-patch` 插件

```
pip install akshare-proxy-patch==0.5.0
```

## 🚀 使用方法（akshare / efinance / yfinance）

1. [点击前往插件官网](https://ak.cheapproxy.net/dashboard/akshare) 获取 `TOKEN`。

2. `akshare` 或 `efinance` 用户：在 **Python 文件最顶部**添加如下代码，并替换 `你的TOKEN`，不需要使用 AI 魔改。

```
# python 文件顶部添加如下代码
# 插件引入和调用一定要放到最顶部！不能在 akshare 或 efinance 之后引入！
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
    fast=True
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

3. `yfinance` 用户：在 Python 文件顶部添加如下代码，并替换 `你的TOKEN`，不需要使用 AI 魔改。

```
# python 文件顶部添加如下代码
# 插件引入和调用一定要放到最顶部！不能在 akshare 或 efinance 之后引入！
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

4. 尽量用 [efinance](https://github.com/Micro-sheep/efinance) 替代 akshare 的部分函数配合插件获取数据，效率更高，更省积分。

## install_patch 参数说明

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
- 参数5：是否启用多线程加速，加速函数列表如下：
  - 所有用到 `fetch_paginated_data` 分页函数的接口，如 `stock_zh_a_spot_em`、`stock_sh_a_spot_em`、`stock_board_industry_cons_em` 等
  - `stock_individual_fund_flow_rank`
  - `stock_sector_fund_flow_rank`
  - `fund_money_fund_info_em`
  - `fund_graded_fund_info_em`
  - `fund_etf_fund_info_em`
  - `fund_fh_em`
  - `fund_cf_em`
  - `fund_fh_rank_em`
  - 如有其他函数加速需求欢迎反馈

## 如何在 aktools 内集成插件？

- `aktools` 想要集成插件，需下载 [akt.py](https://github.com/HelloYie/akshare-proxy-patch/blob/master/examples/aktools/akt.py) 文件，并填入您的 `TOKEN`。
- 然后执行 `python akt.py` 即可启动一个 `http://127.0.0.1:8080/` 服务。只是启动方式不同而已，使用请参考 [aktools 官方文档](https://github.com/akfamily/aktools)。

## 股票数量很多，如何快速拉取数据？

- 尽量使用 `efinance` 替代 `akshare` 来获取数据， `efinance` 内置多线程，效率更高，更省积分。
- 在大规模快速获取数据时，可使用多进程提升效率。 可以参考 [多进程获取数千支股票行情示例](https://github.com/HelloYie/akshare-proxy-patch/blob/master/examples/%E5%B9%B6%E5%8F%91%E8%8E%B7%E5%8F%96%E8%82%A1%E7%A5%A8%E8%A1%8C%E6%83%85/main.py)，修改 `auth_token`，执行 `python main.py` 测试。

## 如何灵活禁用/启用插件？

加入如下代码后插件就会被禁用，[点击查看禁用/启用插件示例](https://github.com/HelloYie/akshare-proxy-patch/blob/master/examples/disable/disable.py)：

```
akshare_proxy_patch.uninstall_patch()
```

## 我没使用 akshare 或 efinance，能集成插件吗？

- 如果使用 Python 语言的 `requests` 库请求接口，插件能自动 hook 住请求，正常工作。
- 如果您使用其他语言或 python 的其他库，可 [手动提取代理](http://101.201.173.125:47001/api/akshare-auth?token=XXX&version=0.5.0) 自行实现封控解除。

## 使用问题交流群

如使用时遇到问题，或对插件有什么意见或建议，可进群交流：

![AvSEuz0JyKKv7f3snJrszkKDhTLAt0jG.webp](https://cdn.nodeimage.com/i/AvSEuz0JyKKv7f3snJrszkKDhTLAt0jG.webp)
