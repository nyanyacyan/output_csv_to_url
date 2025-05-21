# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/utage_csv_to_gss/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/utage_csv_to_drive/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pandas as pd
import time
from datetime import datetime
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.spreadsheet.spreadsheetRead import GetDataGSSAPI
from method.base.decorators.decorators import Decorators
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.base.utils.logger import Logger
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.spreadsheet.spreadsheetRead import GetDataGSSAPI
from method.base.selenium.get_element import GetElement
from method.base.decorators.decorators import Decorators
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.get_gss_df_flow import GetGssDfFlow

# const
from method.const_element import GssInfo, PopUpComment, Element, CommentFlowElement

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ


class GoodFlow:
    def __init__(self, chrome: WebDriver):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

        # タイムスタンプ
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # const
        self.const_gss_info = GssInfo.INSTA.value
        self.popup_cmt = PopUpComment.INSTA.value
        self.const_element = Element.INSTA.value
        self.const_comment = CommentFlowElement.INSTA.value

        # インスタンス
        self.random_sleep = SeleniumBasicOperations(chrome=chrome)
        self.get_element = GetElement(chrome=chrome)
        self.gss_read = GetDataGSSAPI()
        self.gss_write = GssWrite()
        self.gss_check_err_write = GssCheckerErrWrite()
        self.get_gss_df_flow = GetGssDfFlow()

    ####################################################################################
    #! ----------------------------------------------------------------------------------
    # 書込データをスプシに書き込む

    def process(self, target_worksheet_name: str):
        try:
            try:
                # いいねをクリック
                self.get_element.clickElement(by=self.const_element['by_5'], value=self.const_element['value_5'])
                self.logger.info("いいねをクリックしました")
                self.random_sleep._random_sleep(2, 5)

            except NoSuchElementException:
                self.logger.warning("いいねの要素が見つかりませんので「その他」をクリックします")
                self.get_element.clickElement(by=self.const_element['by_5'], value=self.const_element['value_12'])
                self.logger.info("「その他」をクリックしました")
                self.random_sleep._random_sleep(2, 5)

            except Exception as e:
                self.logger.error(f"いいねをクリック中にエラーが発生: {e}")


            # 書込データを取得
            filtered_write_data, target_df = self._get_filtered_write_data(target_worksheet_name=target_worksheet_name)

            # 書込データをDataFrameに変換
            filtered_write_data = pd.DataFrame(filtered_write_data)
            self.logger.debug(f"書込データ: {filtered_write_data}")

            # 書込データが空の場合
            if filtered_write_data.empty:
                self.logger.error("いいねの書込データが空です")
                return None

            # target_dfがある場合
            if target_df is None or target_df.empty:
                # もしtarget_dfがない場合
                self.logger.warning(f"既存データなし")
                None_row_num = 2
            else:
                self.logger.debug(f"既存データあり: {len(target_df)}")
                row_num = len(target_df)
                self.logger.debug(f"書込データの行数: {row_num}")
                None_row_num = row_num + 2

            end_row_num = None_row_num + len(filtered_write_data) + 1
            self.logger.debug(f"書込データの行数: {len(filtered_write_data)}")
            self.logger.debug(f"書込データの行数: {None_row_num} 行目から {end_row_num} 行目に書き込みます。")

            cell = f"A{None_row_num}:D{end_row_num}"
            self.logger.debug(f"書込データのセル: {cell}")
            self.logger.debug(f"書込データ: {target_worksheet_name} の {cell} 行目に書き込みます。")

            # 書込データのDataFrameをGSSへ書き込むためにリスト型に変換
            gss_write_list = filtered_write_data.values.tolist()
            self.logger.debug(f"書込データリスト: {gss_write_list}")

            # GSSへ書込
            self.gss_write.write_input_worksheet( gss_info=self.const_gss_info, worksheet_name=target_worksheet_name, cell=cell, input_data=gss_write_list )
            self.logger.debug(f"書込データ: {target_worksheet_name} の {cell} 行目に書き込みました。")

            self.logger.info(f"いいねユーザーをスプシに書込完了（全{len(filtered_write_data)}行）")
            return filtered_write_data

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

    #! ----------------------------------------------------------------------------------
    # 既存のユーザー名を取得し、書込データをフィルタリングする

    def _get_filtered_write_data(self, target_worksheet_name: str):
        try:
            # 書込データを取得
            write_data = self._generate_write_data()

            # 既存のユーザー名を取得
            existing_username_list, target_df = self._get_written_username_list(target_worksheet_name=target_worksheet_name)
            self.logger.debug(f"既存のユーザー名リスト: {existing_username_list}")

            # 空の場合の処理
            if existing_username_list is None:
                self.logger.warning("スプレッドシートが初期状態です")
                return write_data, None

            # 既に書込済みのユーザー名を除外する
            filtered_write_data = []
            for data in write_data:
                # ユーザー名が既存のユーザー名リストに含まれていない場合
                if data['username'] not in existing_username_list:
                    filtered_write_data.append(data)
                    self.logger.info(f"フィルタリング対象: {data['username']}")
                else:
                    self.logger.warning(f"フィルタリング除外: {data['username']}")

            self.logger.debug(f"フィルタリング後の書込データ: {filtered_write_data}")
            return filtered_write_data, target_df

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

    # ----------------------------------------------------------------------------------
    # 既存のユーザー名を取得する

    def _get_written_username_list(self, target_worksheet_name: str):
        try:
            # 対象のWorksheetの現在のDataFrameを取得
            target_df = self.get_gss_df_flow.no_filter_process(worksheet_name=target_worksheet_name)

            # DataFrameが空か確認（空ならNoneで返す）
            if target_df is None or target_df.empty:
                self.logger.debug(f"{target_worksheet_name} のデータが空のため、処理をスキップします。")
                return None, None

            self.logger.debug(f"{target_worksheet_name}の入力前df: {target_df.head()}")

            # ユーザー名の列を取得
            username_series = target_df[self.const_gss_info['TARGET_INPUT_USERNAME']]
            self.logger.debug(f"ユーザー名のSeries: {username_series}")

            # シリーズの値をリストに変換
            existing_username_list = username_series.tolist()
            self.logger.debug(f"ユーザー名のリスト: {existing_username_list}")

            return existing_username_list, target_df

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

    # ----------------------------------------------------------------------------------
    # いいねのユーザーデータを作成する

    def _generate_write_data(self):
        try:
            try:
                # モーダルを取得
                modal_element = self._get_modal_element()
                self.random_sleep._random_sleep(2, 5)
                self.logger.info("モーダルを取得しました")

            except NoSuchElementException:
                self.logger.warning("いいねの要素が見つかりませんので「その他」をクリックします")
                self.get_element.clickElement(by=self.const_element['by_5'], value=self.const_element['value_12'])
                self.logger.info("「その他」をクリックしました")
                self.random_sleep._random_sleep(2, 5)
                modal_element = self._get_modal_element()
                self.logger.info("モーダルを取得しました")
                self.random_sleep._random_sleep(2, 5)

            except Exception as e:
                self.logger.error(f"いいねをクリック中にエラーが発生: {e}")

            unique_checker = set()
            user_infos = []
            scroll_step = 200
            max_user_count = 10000  # ← ここを目的に応じて変更

            # 初期位置
            scroll_position = 0
            # スクロール対象のモーダルエリア（適宜クラス指定などで調整）
            while len(user_infos) < max_user_count:
                # a_tags = modal_element.find_elements(By.XPATH, './/a[starts-with(@href, "/") and string-length(@href) > 1]')

                a_tags = self.get_element.filterElements(parentElement=modal_element, value=self.const_element['value_11'])
                self.logger.debug(f"取得した要素数: {len(a_tags)}")
                self.logger.debug(f"取得した要素: {a_tags}")
                for a in a_tags:
                    # ユーザーURLの取得
                    user_url = self._get_good_user_url(good_element=a)

                    # ユーザー名の取得
                    username = self._get_good_user_name(good_user_url=user_url)

                    good_dict_data = {
                        "username": username,
                        "user_url": user_url,
                        "like_or_comment": self.const_comment['INPUT_WORD_GOOD'],
                        "timestamp": self.timestamp,
                    }

                    # 重複を除外する
                    if username not in unique_checker:
                        unique_checker.add(username)
                        self.logger.warning(f"ユーザー名: {username} を追加します。")
                        user_infos.append(good_dict_data)
                    else:
                        # 既に存在する場合はスキップ
                        self.logger.debug(f"ユーザー名: {username} は既在するため、スキップします。")

                        # コメントデータをリストに追加

                    # 10000件以上取得した場合はブレーク
                    if len(user_infos) >= max_user_count:
                        break

                # スクロールを小刻みに行う
                scroll_position += scroll_step
                self.logger.debug(f"スクロール位置: {scroll_position}")
                self.chrome.execute_script("arguments[0].scrollTop = arguments[1]", modal_element, scroll_position)
                time.sleep(1)

                # すでに全て読み込み終わっていた場合のブレーク条件
                current_height = self.chrome.execute_script("return arguments[0].scrollHeight", modal_element)
                if scroll_position >= current_height:
                    break

            self.logger.debug(f"いいねのユーザー要素のリスト: {user_infos}")
            return user_infos

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

    # ----------------------------------------------------------------------------------
    # コメント要素からユーザー名を取得する

    def _get_good_user_url(self, good_element: WebElement):
        self.logger.debug(f"コメント要素: {good_element}")
        # self.logger.debug(f"コメント要素のインデックス: {element_num}")
        # ユーザー名を取得
        # comment_a_tag = good_element.find_element(By.XPATH, f'//a[contains(@href, "/") and @role="link"]')

        user_url = good_element.get_attribute('href')
        self.logger.debug(f"ユーザーURL: {user_url}")

        return user_url

    # ----------------------------------------------------------------------------------
    # InstagramのユーザーURLからユーザー名を取得する

    def _get_good_user_name(self, good_user_url: str):
        # URL部分を除去してユーザー名を取得
        username = good_user_url.replace("https://www.instagram.com/", "").strip("/")
        self.logger.info(f"ユーザー名: {username}")
        return username

    # ----------------------------------------------------------------------------------
    # modalを取得

    def _get_modal_element(self) -> WebElement:
        # モーダルの要素を取得
        modal_element = self.get_element.getElement(value=self.const_element['value_9'])
        self.logger.debug(f"モーダル要素: {modal_element}")
        return modal_element

    # ----------------------------------------------------------------------------------
