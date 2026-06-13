##### 1. 启用插件
import akshare_proxy_patch

akshare_proxy_patch.install_patch(
    "101.201.173.125",
    auth_token='你的TOKEN',
    retry=30,
    # 封控的域名列表，可自行调整
    hook_domains=[
      "fund.eastmoney.com",
      "push2.eastmoney.com",
      "push2his.eastmoney.com",
      "emweb.securities.eastmoney.com",
    ],
    fast=True
)
import akshare as ak
df =  ak.fund_etf_hist_em()

###### 2. 禁用插件
akshare_proxy_patch.uninstall_patch()

# 禁用后测试
try:
  df = ak.fund_etf_hist_em()
except Exception as e:
   print('插件被禁用了，这里可能会报错')

##### 3. 再次启用插件，重复上述 1、2 的代码即可
