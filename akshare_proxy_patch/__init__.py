import time
import requests
from requests.adapters import HTTPAdapter

original_send = HTTPAdapter.send


def install_patch(auth_ip, auth_token):
    def patched_send(self, request, **kwargs):
        auth_url = f"http://{auth_ip}:47001/api/akshare-auth"
        url = request.url
        is_hook = (
            ("fund.eastmoney.com" in url)
            or ("push2.eastmoney.com" in url)
            or ("push2his.eastmoney.com" in url)
        )
        for i in range(60):
            try:
                if not is_hook:
                    return original_send(self, request, **kwargs)
                with requests.Session() as s:
                    HTTPAdapter.send = original_send
                    auth_res = s.get(
                        auth_url, params={"token": auth_token}, timeout=5
                    ).json()
                    if not auth_res["ua"]:
                        error_msg = (
                            auth_res.get("error_msg", "")
                            or "未知异常，请联系 cheapproxy.net 客服"
                        )
                        print(error_msg)
                        return None

                    HTTPAdapter.send = patched_send
                request.headers["User-Agent"] = auth_res["ua"]
                cookie_str = f"nid18={auth_res['nid18']}; nid18_create_time={auth_res['nid18_create_time']}"
                request.headers["Cookie"] = cookie_str
                proxy = auth_res["proxy"]
                kwargs["proxies"] = {"http": proxy, "https": proxy}
                kwargs["timeout"] = 8
                return original_send(self, request, **kwargs)
            except Exception as e:
                if not is_hook:
                    time.sleep(0.5)
                HTTPAdapter.send = patched_send

        return original_send(self, request, **kwargs)

    HTTPAdapter.send = patched_send
