# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/ccx_csv_to_drive/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/instagram_list_tool/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, time
import pandas as pd
import concurrent.futures
from typing import Dict
from datetime import datetime, date, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.chrome import ChromeManager
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.spreadsheet.spreadsheetRead import GetDataGSSAPI
from method.base.selenium.get_element import GetElement
from method.base.decorators.decorators import Decorators
from method.base.utils.time_manager import TimeManager
from method.base.selenium.google_drive_download import GoogleDriveDownload
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.select_cell import GssSelectCell
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.utils.popup import Popup
from method.base.selenium.click_element import ClickElement
from method.base.utils.file_move import FileMove
from method.base.selenium.google_drive_upload import GoogleDriveUpload
from method.get_gss_df_flow import GetGssDfFlow
from method.base.selenium.driverWait import Wait
# from method.base.utils.date_manager import DateManager
from method.base.utils.sub_date_mrg import DateManager


# const
from method.const_element import ( GssInfo, LoginInfo, ErrCommentInfo, PopUpComment, Element, )

# flow
# from method.good_flow import GetUserToInsta
from method.comment_flow import CommentFlow
from method.good_flow import GoodFlow

deco = Decorators()

# ----------------------------------------------------------------------------------

# **********************************************************************************
# 一連の流れ


class SingleProcess:
    def __init__(self):
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        self.timestamp = datetime.now()
        self.timestamp_two = self.timestamp.strftime("%Y-%m-%d %H:%M")
        self.date_only_stamp = self.timestamp.date().strftime("%m月%d日")

        # ✅ Chrome の起動をここで行う
        self.chromeManager = ChromeManager()
        self.chrome = self.chromeManager.flowSetupChrome()

        # const
        self.const_gss_info = GssInfo.OUTPUT_CSV.value
        self.const_login_info = LoginInfo.OUTPUT_CSV.value
        self.const_element = Element.OUTPUT_CSV.value
        self.const_err_cmt_dict = ErrCommentInfo.OUTPUT_CSV.value
        self.popup_cmt = PopUpComment.OUTPUT_CSV.value

        # Flow
        self.get_gss_df_flow = GetGssDfFlow()
        # self.get_user_data = GetUserToInsta(chrome=self.chrome)
        self.comment_flow = CommentFlow(chrome=self.chrome)
        self.good_flow = GoodFlow(chrome=self.chrome)

        # インスタンス
        self.login = SingleSiteIDLogin(chrome=self.chrome)
        self.random_sleep = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.selenium = SeleniumBasicOperations(chrome=self.chrome)
        self.gss_read = GetDataGSSAPI()
        self.gss_write = GssWrite()
        self.drive_download = GoogleDriveDownload()
        self.drive_upload = GoogleDriveUpload()
        self.select_cell = GssSelectCell()
        self.gss_check_err_write = GssCheckerErrWrite()
        self.popup = Popup()
        self.click_element = ClickElement(chrome=self.chrome)
        self.file_move = FileMove()
        self.wait = Wait(chrome=self.chrome)
        self.date_manager = DateManager()
        self.select_cell = GssSelectCell()


    # **********************************************************************************
    # ----------------------------------------------------------------------------------

    def _single_process(self):
        """各プロセスを実行する"""
        try:
            id_text = self.const_login_info['ID_TEXT']
            # ログイン
            self.login.flowLoginID(id_text=self.const_login_info['ID_INPUT_TEXT'], pass_text=self.const_login_info['PASS_INPUT_TEXT'], login_info=self.const_login_info)

            # 対象のページが開いているかどうかを確認
            self.get_element.clickElement(by=self.const_element['by_5'], value=self.const_element['value_5'])

            # 詳細検索クリック
            self.get_element.clickElement(by=self.const_element['by_5'], value=self.const_element['value_5'])


            # キーワード欄に入力
            self.get_element.clickClearInput(value=self.const_element['value_1'])


            # 対象の期間をクリック（引数には要素を渡す？）
            self.get_element.clickElement(by=self.const_element['by_5'], value=self.const_element['value_5'])



            # 選択をクリック
            self.get_element.clickElement(by=self.const_element['by_5'], value=self.const_element['value_5'])



            # 検索をクリック（EnterKey可）
            self.get_element.clickElement(by=self.const_element['by_5'], value=self.const_element['value_5'])



            # 要素のリスト取得（テーブルの取得）
            elements = self.get_element.getElements(by=self.const_element['by_2'], value=self.const_element['value_2'])


            csv_list = []
            # 要素１つずつにアクセス
            for element in elements:

                # 国名が書かれている要素を取得
                country_name_element = self.get_element.getElement(by=self.const_element['by_2'], value=self.const_element['value_2'])

                # 国名,抽出
                if country_name_element is None:
                    self.logger.error(f"{self.__class__.__name__} 国名の要素が見つかりませんでした。")
                    continue

                country_name = country_name_element.text
                self.logger.info(f"国名: {country_name}")

                # 記事名(タイトル)が書かれている要素を取得
                title_element = self.get_element.getElement(by=self.const_element['by_2'], value=self.const_element['value_2'])

                # 記事名(タイトル),抽出
                if title_element is None:
                    self.logger.error(f"{self.__class__.__name__} 記事名の要素が見つかりませんでした。")
                    continue

                country_name = title_element.text
                self.logger.info(f"記事名: {country_name}")

                # URLが書かれている要素を取得
                url_element = self.get_element.getElement(by=self.const_element['by_2'], value=self.const_element['value_2'])

                if url_element is None:
                    self.logger.error(f"{self.__class__.__name__} URLの要素が見つかりませんでした。")
                    continue

                # URL,抽出
                url = url_element.get_attribute("href")
                self.logger.info(f"URL: {url}")


                # URLのリプライス（?highlight=ビザ などのおしり部分を削除）


                # 抽出したものを","で結合
                join_element = ",".join(country_name, title_element, url_element)
                self.logger.info(f"結合した要素: {join_element}")

                # リストに追加
                csv_list.append(join_element)

            self.logger.info(f"csv_list: {csv_list}")

            # csvファイルに書き込めるように修正

            # csvファイルに書き込み


        except TimeoutError:
            timeout_comment = "タイムエラー：ログインに失敗している可能性があります。"
            self.logger.error(f"{self.__class__.__name__} {timeout_comment}")

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)


        finally:
            # ✅ Chrome を終了
            self.chrome.quit()
            self.popup.popupCommentOnly( popupTitle=self.popup_cmt["POPUP_COMPLETE_TITLE"], comment=self.popup_cmt["POPUP_COMPLETE_MSG"], )

    # ----------------------------------------------------------------------------------

    def _delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
            self.logger.info(f"指定のファイルの削除を実施: {file_path}")

        else:
            self.logger.error( f"{self.__class__.__name__} ファイルが存在しません: {file_path}" )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# テスト実施

if __name__ == "__main__":

    test_flow = SingleProcess()
    # 引数入力
    test_flow._single_process()
