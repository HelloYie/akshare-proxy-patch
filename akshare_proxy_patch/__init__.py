import time
import threading
import requests
from copy import deepcopy
from requests.adapters import HTTPAdapter

# 备份原始 send
_original_send = HTTPAdapter.send

# 线程局部状态
_thread_state = threading.local()

# 独立 Session：专门用于授权请求（不走 hook）
_auth_session = requests.Session()


def get_auth_config_realtime(auth_url, auth_token):
    """实时获取授权信息（不走全局 hook）"""
    try:
        resp = _auth_session.get(
            auth_url,
            params={"token": auth_token},
            timeout=5,
        )
        data = resp.json()
        if data.get("ua"):
            return data
        error_msg = (
            data.get("error_msg")
            or "接口授权失败，请登录 https://cheapproxy.net 联系客服获取授权码"
        )
        print(f"========={error_msg}========")
    except Exception as e:
        print(f"=========接口授权失败，{e}========")
    return None


def install_patch(auth_ip, auth_token):
    def patched_send(self, request, **kwargs):
        # 如果明确标记跳过 hook，直接原逻辑
        if getattr(_thread_state, "skip_hook", False):
            return _original_send(self, request, **kwargs)

        url = request.url or ""

        is_target = any(
            d in url
            for d in (
                "fund.eastmoney.com",
                "push2.eastmoney.com",
                "push2his.eastmoney.com",
            )
        )

        # 非目标域名直接放行
        if not is_target:
            return _original_send(self, request, **kwargs)

        auth_url = f"http://{auth_ip}:47001/api/akshare-auth"

        # 每次请求都用“独立副本”
        new_request = deepcopy(request)
        new_kwargs = deepcopy(kwargs)

        for _ in range(30):
            try:
                auth_res = get_auth_config_realtime(auth_url, auth_token)
                if auth_res:
                    new_request.headers = deepcopy(request.headers)
                    new_request.headers["User-Agent"] = auth_res["ua"]
                    new_request.headers["Cookie"] = (
                        f"nid18={auth_res['nid18']}; "
                        f"nid18_create_time={auth_res['nid18_create_time']}"
                    )

                    proxy = auth_res["proxy"]
                    new_kwargs["proxies"] = {
                        "http": proxy,
                        "https": proxy,
                    }
                    new_kwargs["timeout"] = 8

                resp = _original_send(self, new_request, **new_kwargs)
                if resp.ok:
                    return resp

            except Exception:
                time.sleep(0.01)

        # 兜底：30 次都失败，走原请求
        return _original_send(self, request, **kwargs)

    HTTPAdapter.send = patched_send
