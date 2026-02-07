import requests
import time
from requests.adapters import HTTPAdapter

original_send = HTTPAdapter.send


def install_patch(auth_token):
    def patched_send(self, request, **kwargs):
        url = request.url
        if "82.push2.eastmoney.com" not in url and "push2his.eastmoney.com" not in url:
            return original_send(self, request, **kwargs)
        for i in range(60):
            try:
                with requests.Session() as s:
                    HTTPAdapter.send = original_send
                    auth_url = "http://akshare.cheapproxy.net/api/akshare-auth"
                    auth_res = s.get(
                        auth_url, params={"token": auth_token}, timeout=5
                    ).json()
                    if not auth_res["ua"]:
                        print("请先登录 https://cheapproxy.net 联系客服获取授权码")
                        return None

                    HTTPAdapter.send = patched_send
                request.headers["User-Agent"] = auth_res["ua"]
                cookie_str = f"nid18={auth_res['nid18']}; nid18_create_time={auth_res['nid18_create_time']}"
                request.headers["Cookie"] = cookie_str
                proxy = auth_res["proxy"]
                kwargs["proxies"] = {"http": proxy, "https": proxy}
                kwargs["timeout"] = 10
                return original_send(self, request, **kwargs)
            except Exception as e:
                time.sleep(1)
                HTTPAdapter.send = patched_send

        return original_send(self, request, **kwargs)

    HTTPAdapter.send = patched_send
