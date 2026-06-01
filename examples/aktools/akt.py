# -*- coding: utf-8 -*-

# 添加插件
import akshare_proxy_patch

akshare_proxy_patch.install_patch(
    "101.201.173.125",
    auth_token="你的TOKEN",
    retry=30,
    # 封控的域名列表，可自行调整
    hook_domains=[
        "fund.eastmoney.com",
        "push2.eastmoney.com",
        "push2his.eastmoney.com",
        "emweb.securities.eastmoney.com",
    ],
)

# 启动 aktools
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "aktools.main:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
        # 根据 CPU 核心数调整，推荐 2×核心数 + 1
        workers=4,
        log_level="info",
    )
