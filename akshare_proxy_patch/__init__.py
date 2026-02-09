import time
import threading
import requests
from requests.adapters import HTTPAdapter

__version__ = "0.2.3"
# 备份 Session 的原始 request 方法，这是所有 requests.get/post 的最终入口
_original_request = requests.Session.request
_auth_session = requests.Session()


class AuthCache:
    def __init__(self):
        self.data = None
        self.expire_at = 0
        self.lock = threading.Lock()
        self.ttl = 20


_cache = AuthCache()


def get_auth_config_with_cache(auth_url, auth_token):
    now = time.time()
    # 1. 检查缓存是否有效
    if _cache.data and now < _cache.expire_at:
        return _cache.data

    # 2. 缓存失效，加锁更新
    with _cache.lock:
        if _cache.data and now < _cache.expire_at:
            return _cache.data

        try:
            resp = _auth_session.get(
                auth_url,
                params={"token": auth_token, "version": __version__},
                timeout=5,
            )
            data = resp.json()
            if data.get("ua"):
                _cache.data = data
                _cache.expire_at = now + _cache.ttl
                return data
            print(f"授权失败: {data.get('error_msg')}")
        except Exception as e:
            print(f"请求授权接口异常: {e}")

        return _cache.data


def install_patch(auth_ip, auth_token):
    def patched_request(self, method, url, **kwargs):
        # 排除非目标域名
        is_target = any(
            d in (url or "")
            for d in [
                "fund.eastmoney.com",
                "push2.eastmoney.com",
                "push2his.eastmoney.com",
            ]
        )

        if not is_target:
            return _original_request(self, method, url, **kwargs)

        auth_url = f"http://{auth_ip}:47001/api/akshare-auth"

        # 重试逻辑
        for _ in range(10):
            auth_res = get_auth_config_with_cache(auth_url, auth_token)
            if not auth_res:
                time.sleep(0.5)
                continue

            # 处理 Headers：确保不破坏业务代码传入的 headers
            headers = kwargs.get("headers") or {}
            headers["User-Agent"] = auth_res["ua"]
            headers["Cookie"] = (
                f"nid18={auth_res['nid18']}; nid18_create_time={auth_res['nid18_create_time']}"
            )
            kwargs["headers"] = headers
            kwargs["proxies"] = {
                "http": auth_res["proxy"],
                "https": auth_res["proxy"],
            }

            if "timeout" not in kwargs:
                kwargs["timeout"] = 8

            try:
                # 调用原始 request 方法
                resp = _original_request(self, method, url, **kwargs)
                if resp.ok:
                    return resp

                # 如果遇到 403 等可能是代理失效
                if resp.status_code == 403:
                    with _cache.lock:
                        _cache.expire_at = 0
            except Exception:
                # 网络异常直接使缓存失效，强制下一个请求换 IP
                with _cache.lock:
                    _cache.expire_at = 0
                time.sleep(0.1)

        # 最终尝试
        return _original_request(self, method, url, **kwargs)

    # 关键：全局替换 Session 的 request 入口
    requests.Session.request = patched_request


# 使用示例
# install_patch("你的IP", "你的TOKEN")
# requests.get("http://fund.eastmoney.com/...")
