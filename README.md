# AkShare Proxy Patch

针对 `akshare` 和 `efinance` 的🐒插件补丁，自动为接口注入请求头，解决 `stock_zh_a_spot_em`、`stock_zh_a_hist`、`get_realtime_quotes` 等东财接口报错问题。

## 安装

1. 安装并升级官方 [akshare](https://github.com/akfamily/akshare) 或 [efinance](https://github.com/Micro-sheep/efinance) 包

2. 安装 `akshare-proxy-patch` 插件

```
pip install akshare-proxy-patch==0.2.13
```

## 使用方法

`akshare` 和 `efinance` 使用方式一致，在文件顶部添加如下代码即可，无需其他额外操作。

```
# python 文件顶部添加如下代码
import akshare_proxy_patch

akshare_proxy_patch.install_patch(
    "101.201.173.125",
    # 免费版为空，付费版填入具体TOKEN
    auth_token="",
    retry=30,
    # 封控的域名列表，可动态调整
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

## install_patch 参数说明

- 参数1：网关
  - 默认为 `101.201.173.125` 不可修改
- 参数2：TOKEN
  - 默认为空，每天可免费使用一定次数。如有更多需求，可[点击此处注册](https://ak.cheapproxy.net/dashboard/akshare)申请正式的 `TOKEN`。
- 参数3：重试次数
  - 默认为30，建议保持不变
- 参数4：封控的域名列表
  - 可点击 `ak` 或 `ef` 函数查看接口源码对应的域名，根据封控情况调整域名可以降低积分消耗。
  - 如只封控 `stock_zh_a_spot_em` 这个接口，`hook_domains` 设置为 `["https://82.push2.eastmoney.com/api/qt/clist/get"]` 即可。

## 如何在 aktools 内集成插件？

需要新建一个 `akt.py` 替换官方的启动方式：

```
# 添加插件
import akshare_proxy_patch

akshare_proxy_patch.install_patch(
    "101.201.173.125",
    # 免费版为空，付费版填入具体TOKEN
    auth_token="",
    retry=30,
    # 封控的域名列表，可动态调整
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

然后执行 `python akt.py` 即可启动并正常使用 `aktools`。

## 我没使用 akshare 或 efinance，能集成插件吗？

- 如果使用 python 语言的 `requests` 库请求东财接口，插件能自动 hook 住请求，正常工作。
- 如果您使用其他语言或 python 的其他库，可 [手动提取代理](http://101.201.173.125:47001/api/akshare-auth?token=&version=0.2.13) 自行实现封控解除。

## 使用问题交流群

如使用时遇到问题，或对插件有什么意见或建议，可进群交流：

![hx8knYwcWWnRjaPzHuWPXajFougAeGc6.webp](https://cdn.nodeimage.com/i/hx8knYwcWWnRjaPzHuWPXajFougAeGc6.webp)
