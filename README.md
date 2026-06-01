# AkShare Proxy Patch

> 针对 [akshare](https://github.com/akfamily/akshare)、[efinance](https://github.com/Micro-sheep/efinance)、[yfinance](https://github.com/ranaroussi/yfinance) 的🐒插件补丁，解决 `stock_zh_a_spot_em`、`stock_zh_a_hist`、`get_realtime_quotes` 等接口报错问题和 Yahoo `YFRateLimitError` 问题。

## ✨ 特性

- 解决 `akshare` 接口报错问题
- 解决 `efinance` 接口报错问题
- 解决 `yfinance` Yahoo接口报错问题

## 📦 安装

1. 安装并升级官方 [akshare](https://github.com/akfamily/akshare) 或 [efinance](https://github.com/Micro-sheep/efinance) 包

2. 安装 `akshare-proxy-patch` 插件

```
pip install akshare-proxy-patch==0.4.2
```

## 🚀 使用方法（akshare / efinance / yfinance）

1. [点击前往插件官网](https://ak.cheapproxy.net/dashboard/akshare) 获取 `TOKEN`。

2. `akshare` 或 `efinance` 用户：在 **Python 文件最顶部**添加如下代码，并替换 `你的TOKEN`。调用非常简单，不需要使用 AI 魔改。

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

3. `yfinance` 用户：在 Python 文件顶部添加如下代码，并替换 `你的TOKEN`。调用非常简单，不需要使用 AI 魔改。

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

## 如何在 aktools 内集成插件？

- `aktools` 想要集成插件，需下载 [akt.py](https://github.com/HelloYie/akshare-proxy-patch/blob/master/examples/aktools/akt.py) 文件，并填入您的 `TOKEN`。
- 然后执行 `python akt.py` 即可启动一个 `http://127.0.0.1:8080/` 服务。只是启动方式不同而已，使用请参考 [aktools 官方文档](https://github.com/akfamily/aktools)。

## 如何多进程使用，快速拉取数据？

- 尽量使用 `efinance` 替代 `akshare` 来获取数据， `efinance` 内置多线程，效率更高，更省积分。
- 在大规模快速获取数据时，仍需要多进程来提升效率。 参考 `examples/并发获取股票行情/` 目录下的 `main.py` 和 `worker.py` 示例，修改 `worker.py` 中的 `auth_token`，执行 `python main.py` 即可。
- `main.py` 负责分割任务和启动多个 `worker.py` 进程，`worker.py` 中引入插件并执行数据获取逻辑，最后将结果合并保存。

## 如何灵活禁用/启用插件？

加入如下代码后插件就会被禁用：

```
import importlib, requests;importlib.reload(requests)
```

下面是插件启用 --> 禁用 --> 再次启用的例子：

```
##### 1. 启用插件
import akshare_proxy_patch

akshare_proxy_patch.install_patch(
    "101.201.173.125",
    auth_token='你的TOKEN',
    retry=30,
    # 封控的域名列表，可自行调整
    hook_domains=[
      "fund.eastmoney.com",
      "push2.eastmoney.com",
      "push2his.eastmoney.com",
      "emweb.securities.eastmoney.com",
    ],
)
import akshare as ak
df =  ak.fund_etf_hist_em()

###### 2. 禁用插件
import importlib, requests;importlib.reload(requests)

# 禁用后测试
try:
  df = ak.fund_etf_hist_em()
except Exception as e:
   print('插件被禁用了，这里可能会报错')

##### 3. 再次启用插件，重复上述 1、2 的代码即可
```

## 我没使用 akshare 或 efinance，能集成插件吗？

- 如果使用 Python 语言的 `requests` 库请求接口，插件能自动 hook 住请求，正常工作。
- 如果您使用其他语言或 python 的其他库，可 [手动提取代理](http://101.201.173.125:47001/api/akshare-auth?token=XXX&version=0.4.2) 自行实现封控解除。

## 使用问题交流群

如使用时遇到问题，或对插件有什么意见或建议，可进群交流：

![5TZKxn1xMXE84yE4Df8wmWC5a6BNy7gs.webp](https://cdn.nodeimage.com/i/5TZKxn1xMXE84yE4Df8wmWC5a6BNy7gs.webp)
