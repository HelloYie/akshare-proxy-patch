import importlib
import sys
import time
import random
import threading

from .akshare_src.func import fetch_paginated_data as _patched_fetch_paginated_data
from .akshare_src.stock.stock_fund_em import (
    stock_individual_fund_flow_rank as _patched_stock_individual_fund_flow_rank,
    stock_sector_fund_flow_rank as _patched_stock_sector_fund_flow_rank,
)
from .akshare_src.fund.fund_em import (
    fund_money_fund_info_em as _patched_fund_money_fund_info_em,
    fund_graded_fund_info_em as _patched_fund_graded_fund_info_em,
    fund_etf_fund_info_em as _patched_fund_etf_fund_info_em,
)
from .akshare_src.fund.fund_fhsp_em import (
    fund_fh_em as _patched_fund_fh_em,
    fund_cf_em as _patched_fund_cf_em,
    fund_fh_rank_em as _patched_fund_fh_rank_em,
)

# 1. 导入必要的库
try:
    from curl_cffi import requests as curl_requests
    from curl_cffi.requests import BrowserType
    from curl_cffi.requests.errors import RequestsError as RequestException
except ImportError:
    raise ImportError("请执行 pip install curl_cffi 来安装依赖")

import requests as std_requests

__version__ = "0.5.0"

# 授权接口固定使用标准 requests，避免干扰
_auth_session = std_requests.Session()

target_browsers = [
    b
    for b in BrowserType.__dict__.values()
    if isinstance(b, str) and (b.startswith("chrome") or b.startswith("edge"))
]

origin_backup = {}


class AuthCache:
    def __init__(self):
        self.data = None
        self.expire_at = 0
        self.lock = threading.Lock()
        self.ttl = 28


_cache = AuthCache()


def get_auth_config_with_cache(auth_url, auth_token):
    now = time.time()
    if _cache.data and now < _cache.expire_at:
        return _cache.data
    with _cache.lock:
        if _cache.data and now < _cache.expire_at:
            return _cache.data
        try:
            resp = _auth_session.get(
                auth_url,
                params={"token": auth_token, "version": __version__},
                timeout=(1.5, 3),
            )
            data = resp.json()
            if data.get("ua"):
                _cache.data = data
                _cache.expire_at = now + _cache.ttl
                return data
            print(f"授权失败: {data.get('error_msg')}")
        except:
            pass
        return _cache.data


default_hook_domains = [
    "fund.eastmoney.com",
    "push2.eastmoney.com",
    "push2his.eastmoney.com",
    "emweb.securities.eastmoney.com",
]


def install_patch(
    auth_ip,
    auth_token="",
    retry=30,
    hook_domains=default_hook_domains,
    timeout=5,
    cookie="",
    fast=True,
):
    # --- 核心改进：备份原始 Session 避开递归死循环 ---
    if not hasattr(std_requests, "_OriginalSession"):
        std_requests._OriginalSession = std_requests.Session

    _CFFIBaseSession = curl_requests.Session

    # 这里的基类改为 std_requests.Session，确保对第三方库的 isinstance 检查通过
    class PatchedSession(std_requests._OriginalSession):
        def request(self, method, url, **kwargs):
            is_target = any(d in (url or "") for d in hook_domains)
            clean_url = (url or "").split("?")[0].lower()

            # --- 情况 1：非目标域名，使用原始 requests 逻辑 ---
            if (
                not is_target
                or clean_url.endswith(".js")
                or clean_url.endswith(".html")
            ):
                kwargs.pop("impersonate", None)  # 移除 curl_cffi 特有参数
                # 显式调用备份的原始 Session 方法，彻底避免递归
                return std_requests._OriginalSession.request(
                    self, method, url, **kwargs
                )

            # --- 情况 2：目标域名，逻辑保持不变 (走 curl_cffi) ---
            auth_url = f"http://{auth_ip}:47001/api/akshare-auth"

            # 这里的逻辑和之前完全一致
            for i in range(retry):
                auth_res = get_auth_config_with_cache(auth_url, auth_token)
                if not auth_res:
                    time.sleep(0.05)
                    continue

                headers = kwargs.get("headers") or {}
                headers["Cookie"] = cookie or auth_res.get("cookie", "")
                kwargs["headers"] = headers
                kwargs["proxies"] = {
                    "http": auth_res["proxy"],
                    "https": auth_res["proxy"],
                }
                kwargs["timeout"] = timeout
                kwargs["impersonate"] = random.choice(target_browsers)

                try:
                    # 对于目标域名，利用 curl_cffi 的 Session 来发起请求
                    with _CFFIBaseSession() as cffi_s:
                        resp = cffi_s.request(method, url, **kwargs)
                        if resp.status_code == 200:
                            return resp
                        with _cache.lock:
                            _cache.expire_at = 0
                except:
                    with _cache.lock:
                        _cache.expire_at = 0
                time.sleep(0.05)

            return std_requests._OriginalSession.request(self, method, url, **kwargs)

    # 定义补丁包装函数
    def patched_get(url, params=None, **kwargs):
        with PatchedSession() as s:
            return s.get(url, params=params, **kwargs)

    def patched_post(url, data=None, json=None, **kwargs):
        with PatchedSession() as s:
            return s.post(url, data=data, json=json, **kwargs)

    def patched_request(method, url, **kwargs):
        with PatchedSession() as s:
            return s.request(method, url, **kwargs)

    # --- 最小化原地注入 ---
    # 仅修改标准 requests 模块的成员引用，不替换 sys.modules["requests"]
    std_requests.Session = PatchedSession
    std_requests.get = patched_get
    std_requests.post = patched_post
    std_requests.request = patched_request

    # 同步修改 curl_requests 以保持库内部一致性
    curl_requests.Session = PatchedSession
    curl_requests.get = patched_get
    curl_requests.post = patched_post

    if fast:
        install_fast_patch()


def install_fast_patch():
    """
    一些函数使用多线程替代分页请求，提升效率
    """
    try:
        akshare = importlib.import_module("akshare")
        # 覆盖已加载的 akshare 模块的 fetch_paginated_data
        for name, mod in list(sys.modules.items()):
            if mod and name.startswith("akshare"):
                if hasattr(mod, "fetch_paginated_data"):
                    origin_backup[(name, "fetch_paginated_data")] = getattr(
                        mod, "fetch_paginated_data"
                    )
                    setattr(mod, "fetch_paginated_data", _patched_fetch_paginated_data)

        origin_backup[("akshare", "stock_individual_fund_flow_rank")] = getattr(
            akshare, "stock_individual_fund_flow_rank"
        )
        setattr(
            akshare,
            "stock_individual_fund_flow_rank",
            _patched_stock_individual_fund_flow_rank,
        )

        origin_backup[("akshare", "stock_sector_fund_flow_rank")] = getattr(
            akshare, "stock_sector_fund_flow_rank"
        )
        setattr(
            akshare,
            "stock_sector_fund_flow_rank",
            _patched_stock_sector_fund_flow_rank,
        )

        origin_backup[("akshare", "fund_money_fund_info_em")] = getattr(
            akshare, "fund_money_fund_info_em"
        )
        setattr(
            akshare,
            "fund_money_fund_info_em",
            _patched_fund_money_fund_info_em,
        )

        origin_backup[("akshare", "fund_graded_fund_info_em")] = getattr(
            akshare, "fund_graded_fund_info_em"
        )
        setattr(
            akshare,
            "fund_graded_fund_info_em",
            _patched_fund_graded_fund_info_em,
        )

        origin_backup[("akshare", "fund_etf_fund_info_em")] = getattr(
            akshare, "fund_etf_fund_info_em"
        )
        setattr(
            akshare,
            "fund_etf_fund_info_em",
            _patched_fund_etf_fund_info_em,
        )

        origin_backup[("akshare", "fund_fh_em")] = getattr(akshare, "fund_fh_em")
        setattr(
            akshare,
            "fund_fh_em",
            _patched_fund_fh_em,
        )

        origin_backup[("akshare", "fund_cf_em")] = getattr(akshare, "fund_cf_em")
        setattr(
            akshare,
            "fund_cf_em",
            _patched_fund_cf_em,
        )

        origin_backup[("akshare", "fund_fh_rank_em")] = getattr(
            akshare, "fund_fh_rank_em"
        )
        setattr(
            akshare,
            "fund_fh_rank_em",
            _patched_fund_fh_rank_em,
        )
    except Exception as e:
        print("启动快速模式失败：", e)


def install_yfinance_patch(
    auth_ip, auth_token="", retry=30, hook_domains=["finance.yahoo.com"]
):
    from .yfinance import install_yfinance_patch_main

    install_yfinance_patch_main(auth_ip, auth_token, retry, hook_domains)


def uninstall_patch():
    """
    卸载插件，恢复原始状态
    """
    import requests

    # 恢复 requests 模块到原始状态
    importlib.reload(requests)
    try:
        # 还原 akshare 模块
        for (mod_name, func_name), original_func in origin_backup.items():
            if mod_name in sys.modules:
                setattr(sys.modules[mod_name], func_name, original_func)
    except Exception as e:
        print("还原 akshare 模块失败：", e)
