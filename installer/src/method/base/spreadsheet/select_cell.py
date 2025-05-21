# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
import pandas as pd
from typing import Dict


# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.errorHandlers import NetworkHandler
from method.base.utils.path import BaseToPath


# ----------------------------------------------------------------------------------
####################################################################################
# **********************************************************************************


class GssSelectCell:
    def __init__(self):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.networkError = NetworkHandler()
        self.path = BaseToPath()

    ####################################################################################
    # ✅ 行のcolumnからセルの列のアルファベットを出力

    def get_cell_address(self, gss_row_dict: Dict, col_name: str, row_num: int):
        col_letter = self._get_col_index(gss_row_dict=gss_row_dict, col_name=col_name)
        cell_address = f"{col_letter}{row_num + 1}"
        self.logger.debug(f'指定のアドレス: {cell_address}')
        return cell_address

    ####################################################################################
    # ✅ 行のcolumnからセルの列のアルファベットを出力

    def get_cell_address_add_col(self, col_num: int, col_name: str, row_num: int):
        col_letter = self._get_col_index_col_exists(col_num=col_num, col_name=col_name)
        cell_address = f"{col_letter}{row_num + 1}"
        self.logger.debug(f'指定のアドレス: {cell_address}')
        return cell_address

    ####################################################################################
    # ----------------------------------------------------------------------------------
    # 1始まりのカラム番号を Excel の A, B, C の形式に変換
    def _col_number_to_letter(self, col_num: int):
        letter = ""
        while col_num > 0:
            col_num, remainder = divmod(col_num -1, 26)
            # chr() は、ASCIIコード（数値）を文字に変換する関数  chr(65)→"A" chr(66)→"B"
            letter = chr(65 + remainder) + letter
        return letter

    # ----------------------------------------------------------------------------------
    # 行のcolumnからセルの列のアルファベットを出力

    def _get_col_index(self, gss_row_dict: Dict, col_name: str):
        col_num = list(gss_row_dict.keys()).index(col_name) + 1
        col_letter = self._col_number_to_letter(col_num=col_num)
        self.logger.debug(f'{col_name} は左から {col_num} 列目 ({col_letter}) にあります。')
        return col_letter

    # ----------------------------------------------------------------------------------
    # 行のcolumnからセルの列のアルファベットを出力

    def _get_col_index_col_exists(self, col_num: int, col_name: str):
        col_letter = self._col_number_to_letter(col_num=col_num)
        self.logger.debug(f'{col_name} は左から {col_num} 列目 ({col_letter}) にあります。')
        return col_letter

    # ----------------------------------------------------------------------------------
    # 対象のWorksheetのAの値がNoneになっている行を取得

    def _get_none_row_index(self, worksheet_name: str):
        # worksheet_nameのA列の値を取得
        input_str_list = list(filter(None, worksheet_name.col_values(1)))
        self.logger.debug(f"取得したリスト: {input_str_list}")

        # 取得したリストの長さを取得
        row_index = len(input_str_list) + 1
        self.logger.debug(f"最初にNoneになっている行数: {row_index}")
        return row_index

    # ----------------------------------------------------------------------------------
    # 貼り付ける範囲を取得

    def _generate_write_range(self, existing_data_df:pd.DataFrame, start_cell_str: str, start_cell_int: int, end_cell_str: str):
        # もしdfがNoneまたは空の場合
        if existing_data_df is None or existing_data_df.empty:
            self.logger.warning("対象のdfが空です。")
            row_none_num = 2
        else:
            # 既存データからの行数から最初のNoneの行数を取得
            row_none_num = len(existing_data_df.columns) + 2
            self.logger.debug(f"最初にNoneになっている行数: {row_none_num}")

        start_cell = f"{start_cell_str}{start_cell_int}"

        end_cell_int = row_none_num + start_cell_int
        end_cell = f"{end_cell_str}{end_cell_int}"
        cell_range = f"{start_cell}:{end_cell}"
        self.logger.debug(f"書き込み範囲: {cell_range}")
        return cell_range

    # ----------------------------------------------------------------------------------
