# !/usr/bin/env python
"""
Date: 2025/3/10 18:00
Desc: 通用帮助函数
"""

import math
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

import pandas as pd

from akshare.utils import http
from akshare.utils.tqdm import get_tqdm


def _get_page(url: str, params: Dict):
    """
    取一页东方财富分页数据；每次新建连接，失败时按 http.request_with_retry 的策略重试
    :return: 响应对象
    :rtype: requests.Response
    """
    r = http.request_with_retry("get", url, params=params, fresh_session=True)
    r.raise_for_status()
    return r


def fetch_paginated_data(url: str, base_params: Dict):
    """
    东方财富-分页获取数据并合并结果
    https://quote.eastmoney.com/f1.html?newcode=0.000001
    :param url: 股票代码
    :type url: str
    :param base_params: 基础请求参数
    :type base_params: dict
    :return: 合并后的数据
    :rtype: pandas.DataFrame
    """
    # 复制参数以避免修改原始参数
    params = base_params.copy()
    # 获取第一页数据，用于确定分页信息
    r = _get_page(url, params)
    data_json = r.json()
    # 计算分页信息
    per_page_num = len(data_json["data"]["diff"])
    total_page = math.ceil(data_json["data"]["total"] / per_page_num)
    # 存储所有页面数据
    temp_list = []
    # 添加第一页数据
    temp_list.append(pd.DataFrame(data_json["data"]["diff"]))
    # 获取进度条
    tqdm = get_tqdm()
    # 并发获取剩余页面；每个任务使用独立参数，避免线程间共享可变状态。
    def fetch_page(page: int):
        page_params = base_params.copy()
        page_params.update({"pn": page})
        # 保留原有随机延迟策略，降低请求过于频繁的概率。
        time.sleep(random.uniform(0.5, 1.5))
        r = _get_page(url, page_params)
        return pd.DataFrame(r.json()["data"]["diff"])

    pages = range(2, total_page + 1)
    if pages:
        # 固定并发上限，避免页数较多时创建过多线程。
        with ThreadPoolExecutor(max_workers=min(8, len(pages))) as executor:
            futures = {executor.submit(fetch_page, page): page for page in pages}
            page_results = {}
            for future in tqdm(as_completed(futures), total=len(futures), leave=False):
                page_results[futures[future]] = future.result()
        # 按页码恢复原顺序，保持合并及相同排序键下的数据顺序不受并发完成顺序影响。
        temp_list.extend(page_results[page] for page in pages)
    # 合并所有数据
    temp_df = pd.concat(temp_list, ignore_index=True)
    temp_df["f3"] = pd.to_numeric(temp_df["f3"], errors="coerce")
    temp_df = temp_df.sort_values(by=["f3"], ascending=False, ignore_index=True)
    temp_df = temp_df.reset_index()
    temp_df["index"] = temp_df["index"].astype(int) + 1
    return temp_df


def set_df_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """
    设置 pandas.DataFrame 为空的情况
    :param df: 需要设置命名的数据框
    :type df: pandas.DataFrame
    :param cols: 字段的列表
    :type cols: list
    :return: 重新设置后的数据
    :rtype: pandas.DataFrame
    """
    if df.shape == (0, 0):
        return pd.DataFrame(data=[], columns=cols)
    else:
        df.columns = cols
        return df
