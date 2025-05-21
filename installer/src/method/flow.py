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
        self.const_gss_info = GssInfo.INSTA.value
        self.const_login_info = LoginInfo.INSTA.value
        self.const_element = Element.INSTA.value
        self.const_err_cmt_dict = ErrCommentInfo.INSTA.value
        self.popup_cmt = PopUpComment.INSTA.value

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
            #* 今回はログインあとのフロートする
            # GSSよりデータ取得→dfを作成
            target_df = self.get_gss_df_flow.process(worksheet_name=self.const_gss_info['TARGET_WORKSHEET_NAME'])
            account_info = self.get_gss_df_flow.get_account_process(worksheet_name=self.const_gss_info['ACCOUNT_WORKSHEET_NAME'])

            # ログイン
            self.login.flowLoginID(id_text=account_info['GSS_ID_TEXT'], pass_text=account_info['GSS_PASS_TEXT'], login_info=self.const_login_info)

            # 対象のページが開いているかどうかを確認
            self.wait.canWaitClick(value=self.const_element['value_1'])

            account_process_count = 1
            # ターゲットユーザーのURLリストを下に下記のフローを回す
            for index, row in target_df.iterrows():
                self.logger.debug(f"{account_process_count} / {len(target_df)} ユーザーアカウント処理開始")
                row_num = index + 1
                row_dict = row.to_dict()
                self.logger.debug(f"row_dict: {row_dict}")

                target_user_url = row_dict[self.const_gss_info["TARGET_USER_URL"]]
                start_daytime = row_dict[self.const_gss_info["START_DAYTIME"]]
                running_date = row_dict[self.const_gss_info["RUNNING_DATE"]]
                write_error = row_dict[self.const_gss_info["WRITE_ERROR"]]
                target_worksheet_url = row_dict[self.const_gss_info["TARGET_WORKSHEET_URL"]]
                target_worksheet_name = row_dict[self.const_gss_info["TARGET_COLUMN_WORKSHEET_NAME"]]


                # アナウンス
                self.logger.info(f"【{index + 1}つ目】の実行  URL: {target_user_url}")

                # それぞれ書き出すセルアドレスを取得
                gss_date_cell = self.select_cell.get_cell_address(gss_row_dict=row_dict, col_name=self.const_gss_info["RUNNING_DATE"], row_num=row_num)
                gss_err_cell = self.select_cell.get_cell_address(gss_row_dict=row_dict, col_name=self.const_gss_info["WRITE_ERROR"], row_num=row_num)
                self.logger.debug(f"\ntarget_user_url: {target_user_url}\nstart_daytime: {start_daytime}\nrunning_date: {running_date}\nwrite_error: {write_error}\ntarget_worksheet_url: {target_worksheet_url}\ntarget_worksheet_name: {target_worksheet_name}\n")
                self.logger.debug(f"実施日: {gss_date_cell}\nエラー記入箇所: {gss_err_cell}")

                if start_daytime == "":
                    self.logger.debug(f"スプシの{index + 1}番目の「取得開始日時」が入力されてません: {start_daytime}")
                    # 開始日付が空白の場合は、エラーにする→POPUP
                    self.popup.popupCommentOnly( title=self.popup_cmt['POPUP_TITLE_SHEET_INPUT_ERR'], comment=self.popup_cmt['POPUP_TITLE_SHEET_START_DATE'])
                    raise

                # アカウント毎WSフォーマットリスト
                new_ws_col= [self.const_gss_info['TARGET_INPUT_USERNAME'], self.const_gss_info['TARGET_INPUT_USER_URL'], self.const_gss_info['TARGET_INPUT_TYPE'], self.const_gss_info['TARGET_INPUT_DATE']]
                self.logger.debug(f"new_ws_col: {new_ws_col}")

                # 対象のワークシート存在確認
                self.gss_write._check_ws(gss_info=self.const_gss_info, ws_name=target_worksheet_name, col_list=new_ws_col)

                # 新しいタブを開いてURLにアクセス
                main_window = self.chrome.current_window_handle
                self.get_element._open_new_page(url=target_user_url)
                self.random_sleep._random_sleep(2, 5)
                #TODO ここに要素が出てから出ないとダメかも

                # ピン留めされた投稿数を取得
                pin_element = self.get_element.getElements(by=self.const_element['by_2'], value=self.const_element['value_2'])
                if not pin_element:
                    self.logger.debug(f"ピン留めされた投稿はありません")
                    pin_count = 0
                else:
                    pin_count = len(pin_element)
                    self.logger.debug(f"ピン留めされた投稿要素: {pin_element}")
                    self.logger.debug(f"【{index + 1}つ目】ピン留めされた投稿数: {pin_count}つ")

                # 最初の投稿をクリック
                self.get_element.clickElement(value=self.const_element['value_3'])
                self.random_sleep._random_sleep(2, 5)

                count = 0
                # pin_count分は除外
                while True:
                    self.logger.info(f"count: {count + 1} 回目 / ピン留め数: {pin_count}個: ループ処理開始")

                    # 日付を取得する
                    post_date_str = self.get_element._get_attribute_to_element(by=self.const_element['by_4'], value=self.const_element['value_4'], attribute_value='datetime')
                    self.logger.debug(f"投稿日時: {post_date_str}")
                    self.logger.debug(f"投稿日時の型: {type(post_date_str)}")

                    # post_date投稿日時をdatetime型に変換
                    post_date = datetime.strptime(post_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    self.logger.debug(f"修正した取得した投稿日時の型: {type(post_date)}")

                    # start_daytimeとend_daytimeの差分（取得したい日付リスト生成）→日付データをdatetime型に変換
                    replace_start_date = self.date_manager._replace_date(date_str=start_daytime)
                    self.logger.debug(f"取得した投稿日時: {type(post_date)} {post_date}, {type(replace_start_date)} {replace_start_date}")

                    # 日付突合
                    if replace_start_date <= post_date:
                        self.logger.info(f"日付チェックOK: {post_date}")
                        self.random_sleep._random_sleep(2, 5)

                        #* コメントFlowの実施
                        self.comment_flow.process(target_worksheet_name=target_worksheet_name)
                        self.random_sleep._random_sleep(2, 5)


                        #* いいねFlowの実施
                        #TODO 要素があるまで待機仕様
                        self.good_flow.process(target_worksheet_name=target_worksheet_name)
                        self.random_sleep._random_sleep(2, 5)

                        # いいねのモーダルを閉じる（close）
                        ActionChains(self.chrome).send_keys(Keys.ESCAPE).perform()
                        self.logger.debug(f"いいねのモーダルを閉じる")
                        self.random_sleep._random_sleep(2, 5)

                        # 次へのボタンを押下
                        ActionChains(self.chrome).send_keys(Keys.ARROW_RIGHT).perform()
                        self.logger.debug(f"次へのボタンを押下")
                        self.random_sleep._random_sleep(2, 5)

                        # カウントがピン留めされている数よりも少ない場合には追加する
                        if count <= pin_count:
                            self.logger.debug(f"ピン留め投稿分: {count}")
                            count += 1
                            self.logger.info(f"ピン留めの上限に達していないため再度ループに戻ります: {count}回目の実施")
                            continue
                        else:
                            self.logger.debug(f"ピン留め分のスキップは上限に達しています: {count}")
                            continue



                    # 日付チェックNGフローの実行
                    else:
                        self.logger.warning(f"指定した日付以前の投稿を検知: {post_date}")
                        if count <= pin_count:
                            self.logger.info(f"ピン留め投稿分のためスキップします: {count}")

                            # 次へのボタンを押下
                            ActionChains(self.chrome).send_keys(Keys.ARROW_RIGHT).perform()
                            self.logger.debug(f"次へのボタンを押下")
                            self.random_sleep._random_sleep(2, 5)

                            count += 1
                            continue
                        else:
                            self.logger.warning(f"日付が指定以前の投稿になったため、ループを終了して次のユーザーに移ります: {post_date}")
                            break

                # 投稿完了→スプシに日付の書込
                self.logger.debug(f"投稿完了→スプシに日付の書込")
                self.logger.debug(f"cell: {gss_date_cell}")
                self.gss_write.write_data_by_url(gss_info=self.const_gss_info, cell=gss_date_cell, input_data=self.timestamp)

                # 対象のタブを閉じる
                self.chrome.close()
                self.chrome.switch_to.window(main_window)
                self.logger.debug(f"タブを閉じました: {target_user_url}")
                self.logger.warning(f"【{account_process_count + 1}つ目】処理完了  URL: {target_user_url}")
                account_process_count += 1

        except TimeoutError:
            timeout_comment = "タイムエラー：ログインに失敗している可能性があります。"
            self.logger.error(f"{self.__class__.__name__} {timeout_comment}")
            # エラータイムスタンプ
            self.gss_write.write_data_by_url( gss_info=self.const_gss_info, cell=gss_date_cell, input_data=self.timestamp_two )

            # エラーコメント
            self.gss_write.write_data_by_url( gss_info=self.const_gss_info, cell=gss_err_cell, input_data="NG" )


        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

            # エラータイムスタンプ
            self.logger.debug(f"self.timestamp: {self.timestamp}")
            self.gss_write.write_data_by_url( gss_info=self.const_gss_info, cell=gss_date_cell, input_data=self.timestamp_two )

            # エラーコメント
            self.gss_write.write_data_by_url( gss_info=self.const_gss_info, cell=gss_err_cell, input_data=process_error_comment )

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
