import time
import threading
from curl_cffi import requests

__version__ = "0.3.0"
_original_request = requests.Session.request
_auth_session = requests.Session()


class AuthCache:
    def __init__(self):
        self.data = None
        self.expire_at = 0
        self.lock = threading.Lock()
        self.ttl = 30


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
                timeout=(1.5, 3),
            )
            data = resp.json()
            if data.get("proxy"):
                _cache.data = data
                _cache.expire_at = now + _cache.ttl
                return data
            print(f"授权失败: {data.get('error_msg')}")
        except Exception as e:
            print(f"请求授权接口异常: {e}")

        return _cache.data


def install_yfinance_patch_main(auth_ip, auth_token="", retry=30, hook_domains=[]):
    def patched_request(self, method, url, **kwargs):
        # 排除非目标域名
        is_target = any(d in (url or "") for d in hook_domains)

        if not is_target:
            return _original_request(self, method, url, **kwargs)

        auth_url = f"http://{auth_ip}:47001/api/yfinance-auth"

        # 重试逻辑
        for _ in range(retry):
            auth_res = get_auth_config_with_cache(auth_url, auth_token)
            if not auth_res:
                time.sleep(0.05)
                continue

            kwargs["proxies"] = {
                "http": auth_res["proxy"],
                "https": auth_res["proxy"],
            }

            kwargs["timeout"] = (2.5, 5)

            try:
                # 调用原始 request 方法
                resp = _original_request(self, method, url, **kwargs)
                if resp.ok:
                    try:
                        content_type = resp.headers.get("Content-Type").lower()
                        if "json" not in content_type:
                            return resp
                        _ = resp.json()
                        return resp
                    except:
                        pass
                with _cache.lock:
                    _cache.expire_at = 0
                time.sleep(0.05)
            except Exception:
                with _cache.lock:
                    _cache.expire_at = 0
                time.sleep(0.05)
        return _original_request(self, method, url, **kwargs)

    requests.Session.request = patched_request
