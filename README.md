# AkShare Proxy Patch
针对 AkShare 的底层补丁，自动为东财等接口注入代理认证头，从而避免 `stock_zh_a_spot_em` 等方法报错。

## 安装

```
pip install --upgrade akshare-proxy-patch
```

## 使用

1. 访问 https://cheapproxy.net 联系客服（备注: token），获取授权码 `AUTH_IP` 和 `AUTH_TOKEN`

2. 将 akshare 升级到最新

```
pip install --upgrade akshare
```

3. 在使用 akshare 文件顶部添加下面的内容 
```
import akshare_proxy_patch

akshare_proxy_patch.install_patch("AUTH_IP", "AUTH_TOKEN")


# import akshare as ak
# df = ak.stock_zh_a_spot_em()
# 你的其他代码......
```

# 使用问题交流群

![E8B03n88UCIUeoQ9p4Z4wx6B9Xop8kR2.webp](https://cdn.nodeimage.com/i/E8B03n88UCIUeoQ9p4Z4wx6B9Xop8kR2.webp)