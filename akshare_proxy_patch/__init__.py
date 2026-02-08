import time
import threading
import requests
from requests.adapters import HTTPAdapter

# 1. 备份原始发送方法
original_send = HTTPAdapter.send

# 2. 线程本地变量：用于标记当前线程是否正在请求“授权接口”，防止递归死循环
_thread_status = threading.local()


def get_auth_config_realtime(auth_url, auth_token):
    """
    实时获取授权信息，不使用缓存。
    """
    # 标记当前线程进入“授权请求状态”
    _thread_status.is_authorizing = True
    try:
        # 这里的请求会进入 patched_send，但因为 is_authorizing 为 True，会走原逻辑
        resp = requests.get(auth_url, params={"token": auth_token}, timeout=5)
        data = resp.json()
        if data.get("ua"):
            return data
    except Exception as e:
        print(f"[Hook Error] 实时获取授权失败: {e}")
    finally:
        # 请求结束，重置标志位
        _thread_status.is_authorizing = False
    return None


def install_patch(auth_ip, auth_token):
    """安装全局 Hook"""

    def patched_send(self, request, **kwargs):
        # 防止递归：如果当前请求是由 get_auth_config 发出的，直接走原逻辑
        if getattr(_thread_status, "is_authorizing", False):
            return original_send(self, request, **kwargs)
        url = request.url
        # 需要hook的域名列表
        is_target = any(
            domain in url
            for domain in [
                "fund.eastmoney.com",
                "push2.eastmoney.com",
                "push2his.eastmoney.com",
            ]
        )

        # 非目标域名，正常放行
        if not is_target:
            return original_send(self, request, **kwargs)

        auth_url = f"http://{auth_ip}:47001/api/akshare-auth"

        # 需要 patch 的接口，重试接口
        for i in range(30):
            try:
                auth_res = get_auth_config_realtime(auth_url, auth_token)
                if auth_res:
                    request.headers["User-Agent"] = auth_res["ua"]
                    request.headers["Cookie"] = (
                        f"nid18={auth_res['nid18']}; nid18_create_time={auth_res['nid18_create_time']}"
                    )
                    proxy = auth_res["proxy"]
                    kwargs["proxies"] = {"http": proxy, "https": proxy}
                    kwargs["timeout"] = 8
                else:
                    print(f"[Hook Warning] 无法获取授权信息，将使用原始请求: {url}")
                # 调用原始 send 方法完成请求
                response = original_send(self, request, **kwargs)
                if response.ok:
                    return response
            except:
                time.sleep(0.01)

    # 关键：全局替换 HTTPAdapter 的 send 方法
    HTTPAdapter.send = patched_send
