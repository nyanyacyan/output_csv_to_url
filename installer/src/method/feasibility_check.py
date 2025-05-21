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



# const
from method.const_element import (
    GssInfo,
    LoginInfo,
    ErrCommentInfo,
    PopUpComment,
    Element,
)

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ


class TestSingleProcess:
    def __init__(self):
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        self.timestamp = datetime.now()
        self.timestamp_two = self.timestamp.strftime("%Y-%m-%d %H:%M")
        self.date_only_stamp = self.timestamp.date().strftime("%m月%d日")

        # const
        self.const_gss_info = GssInfo.INSTA.value
        self.const_login_info = LoginInfo.INSTA.value
        self.const_element = Element.INSTA.value
        self.const_err_cmt_dict = ErrCommentInfo.INSTA.value
        self.popup_cmt = PopUpComment.INSTA.value

        # インスタンス

    # **********************************************************************************
    # ----------------------------------------------------------------------------------
    # IDとPassはenvから取得

    def _env_single_process(self):
        """各プロセスを実行する"""

        # ✅ Chrome の起動をここで行う
        self.chromeManager = ChromeManager()
        self.chrome = self.chromeManager.flowSetupChrome()

        try:
            # インスタンスの作成 (chrome を引数に渡す)
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

            # URLのアクセス→ID入力→Passの入力→ログイン
            self.login.flowLoginID( login_info=self.const_login_info, )


            # 虫眼鏡をクリック
            self.get_element.clickElement(by=self.const_element['by_1'], value=self.const_element['value_1'])

            # ユーザー名を入力した後にenter keyを入力
            self.get_element.input_after_enter_key(by=self.const_element['by_2'], value=self.const_element['value_2'], inputText=self.const_element['TEST_USERNAME'])

            # 最初の投稿をクリック
            self.get_element.clickElement(by=self.const_element['by_3'], value=self.const_element['value_3'])

            # コメントユーザーを取得
            elements = self.chrome.find_elements(By.XPATH, '//a[@role="link" and normalize-space(text()) != ""]')

            usernames = []
            seen = set()  # 重複排除

            for el in elements:
                href = el.get_attribute("href")
                if href:
                    # 例: https://www.instagram.com/mon_guchi/
                    username = href.replace("https://www.instagram.com/", "").strip("/")
                    if username and username not in seen:
                        usernames.append(username)
                        seen.add(username)

            # 次へをクリック
            # self.get_element.clickElement(value=self.const_element['value_6'])

            # 日付データを取得
            # self.get_element._get_attribute_to_element(by=self.const_element['by_4'], value=self.const_element['value_4'], attribute_value='datetime')

            # いいねをクリック
            self.get_element.clickElement(by=self.const_element['by_5'], value=self.const_element['value_5'])

            # いいねのリストを取得

            modal = self.chrome.find_element(By.XPATH, '//div[@role="dialog"]//div[contains(@style, "overflow")]')

            # set()は{}にどんどん入れ込む→同じものは入れない
            seen_users = set()
            all_usernames = []
            scroll_step = 300
            max_user_count = 10000  # ← ここを目的に応じて変更

            # 初期位置
            scroll_position = 0
            # スクロール対象のモーダルエリア（適宜クラス指定などで調整）
            while len(all_usernames) < max_user_count:
                a_tags = modal.find_elements(By.XPATH, './/a[starts-with(@href, "/") and string-length(@href) > 1]')

                for a in a_tags:
                    href = a.get_attribute("href")
                    if (
                        href and
                        href.startswith("https://www.instagram.com/") and
                        href not in seen_users
                    ):
                        seen_users.add(href)
                        username = href.replace("https://www.instagram.com/", "").strip("/")
                        all_usernames.append(username)

                        if len(all_usernames) >= max_user_count:
                            break

                # スクロールを小刻みに行う
                scroll_position += scroll_step
                self.logger.debug(f"スクロール位置: {scroll_position}")
                self.logger.debug(f"取得したユーザー名: {all_usernames} 合計: {len(set(all_usernames))}件")
                self.chrome.execute_script("arguments[0].scrollTop = arguments[1]", modal, scroll_position)
                time.sleep(1)

                # すでに全て読み込み終わっていた場合のブレーク条件
                current_height = self.chrome.execute_script("return arguments[0].scrollHeight", modal)
                if scroll_position >= current_height:
                    break


            #TODO スライドする

            #TODO いいねリストを取得

            #TODO スライドする

            #TODO ピン留めを取得


        except Exception as e:
            process_error_comment = (
                f"{self.__class__.__name__} 処理中にエラーが発生 {e}"
            )
            self.logger.error(process_error_comment)

            # # エラータイムスタンプ
            # self.logger.debug(f"self.timestamp: {self.timestamp}")
            # self.gss_write.write_data_by_url(
            #     gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp_two
            # )

            # # エラーコメント
            # self.gss_write.write_data_by_url(
            #     gss_info=gss_info, cell=err_cmt_cell, input_data=process_error_comment
            # )

        # finally:
        #     delete_count = 0
        #     for upload_path in upload_path_list:
        #         self._delete_file(upload_path)  # CSVファイルを消去
        #         delete_count += 1
        #         self.logger.info(f"{delete_count} つ目のCSVファイルの削除を実施")

            # ✅ Chrome を終了
            self.chrome.quit()

    # ----------------------------------------------------------------------------------

    def _delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
            self.logger.info(f"指定のファイルの削除を実施: {file_path}")

        else:
            self.logger.error(
                f"{self.__class__.__name__} ファイルが存在しません: {file_path}"
            )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# テスト実施

if __name__ == "__main__":

    test_flow = TestSingleProcess()
    # 引数入力
    test_flow._env_single_process()
