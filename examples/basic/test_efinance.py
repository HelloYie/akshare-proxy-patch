import akshare_proxy_patch

akshare_proxy_patch.install_patch(
    "101.201.173.125",
    auth_token="你的TOKEN",
    retry=30,
    hook_domains=[
        "fund.eastmoney.com",
        "push2.eastmoney.com",
        "push2his.eastmoney.com",
        "emweb.securities.eastmoney.com",
        "searchapi.eastmoney.com/api/suggest/get",
        "push2delay.eastmoney.com/api/qt/clist/get"
    ],
)

import efinance as ef

df = ef.stock.get_quote_history('600519')
print(df)
