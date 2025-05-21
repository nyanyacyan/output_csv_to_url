# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time, random
from typing import Dict, Callable
from datetime import datetime


# 自作モジュール
from .logger import Logger


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class DateManager:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()


        self.now = datetime.now()

    # ----------------------------------------------------------------------------------
    # ランダムな待機をする


    def _replace_date(self, date_str, now_date_object: str = "/") -> datetime:
        try:
            # すでに datetime 型ならそのまま返す
            if isinstance(date_str, datetime):
                self.logger.debug("すでに datetime 型です")
                return date_str

            # 文字列の場合のみ処理を行う
            if now_date_object == '/':
                date_obj = datetime.strptime(date_str, "%Y/%m/%d")
            elif now_date_object == '-':
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            elif now_date_object == '.':
                date_obj = datetime.strptime(date_str, "%Y.%m.%d")
            elif now_date_object == '_':
                date_obj = datetime.strptime(date_str, "%Y_%m_%d")
            else:
                self.logger.error("不正な引数が渡されました")
                return None

            return date_obj

        except Exception as e:
            self.logger.error(f"日付変換エラー: {e}")
            return None


    # ----------------------------------------------------------------------------------
