# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/ccx_csv_to_drive/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/output_csv_to_url/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.chrome import ChromeManager
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.selenium.get_element import GetElement
from method.base.decorators.decorators import Decorators
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.utils.popup import Popup
from method.base.selenium.click_element import ClickElement
from method.base.utils.fileWrite import FileWrite

# flow
from method.flow_asia_travel_first import FlowAsiaTravelFirst
from method.flow_asia_travel_second import FlowAsiaTravelSecond
from method.flow_ja_automakers import FlowJaAutomakers
from method.flow_trump import FlowTrump
from method.flow_china_ev import FlowChinaEV
from method.flow_korea import FlowKorea
from method.flow_asia_train import FlowAsiaTrain
from method.flow_ja_asia_entry import FlowJaAsiaEntry

# const
from method.const_element import ( CsvInfo, LoginInfo, ErrCommentInfo, PopUpComment, Element, )

# flow

deco = Decorators()

# ----------------------------------------------------------------------------------

# **********************************************************************************
# 一連の流れ


class SingleProcess:
    def __init__(self):
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        self.timestamp = datetime.now()
        self.timestamp_two = self.timestamp.strftime("%Y-%m-%d_%H-%M")
        self.date_only_stamp = self.timestamp.date().strftime("%m月%d日")

        # ✅ Chrome の起動をここで行う
        self.chromeManager = ChromeManager()
        self.chrome = self.chromeManager.flowSetupChrome()

        # const
        self.const_login_info = LoginInfo.OUTPUT_CSV.value
        self.const_element = Element.OUTPUT_CSV.value
        self.const_err_cmt_dict = ErrCommentInfo.OUTPUT_CSV.value
        self.popup_cmt = PopUpComment.OUTPUT_CSV.value
        self.const_csv_info = CsvInfo.OUTPUT_CSV.value

        # インスタンス
        self.login = SingleSiteIDLogin(chrome=self.chrome)
        self.random_sleep = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.selenium = SeleniumBasicOperations(chrome=self.chrome)
        self.popup = Popup()
        self.click_element = ClickElement(chrome=self.chrome)
        self.file_write = FileWrite()

        # flow
        self.flow_asia_travel_first = FlowAsiaTravelFirst(chrome=self.chrome)
        self.flow_asia_travel_second = FlowAsiaTravelSecond(chrome=self.chrome)
        self.flow_ja_automakers = FlowJaAutomakers(chrome=self.chrome)
        self.flow_trump = FlowTrump(chrome=self.chrome)
        self.flow_china_ev = FlowChinaEV(chrome=self.chrome)
        self.flow_korea = FlowKorea(chrome=self.chrome)
        self.flow_asia_train = FlowAsiaTrain(chrome=self.chrome)
        self.flow_ja_asia_entry = FlowJaAsiaEntry(chrome=self.chrome)

    # **********************************************************************************
    # ----------------------------------------------------------------------------------

    def _single_process(self):
        """各プロセスを実行する"""
        try:
            # 引数にキーワード、期間、
            # ログイン
            self.login.flowLoginID(id_text=self.const_login_info['ID_INPUT_TEXT'], pass_text=self.const_login_info['PASS_INPUT_TEXT'], login_info=self.const_login_info)
            self.random_sleep._random_sleep(2, 5)

            # ログイン移行画面があるか確認
            try:
                login_after_element = self.get_element.getElement(by=self.const_login_info['LOGIN_AFTER_ELEMENT_BY'], value=self.const_login_info['LOGIN_AFTER_ELEMENT_VALUE'])
            except NoSuchElementException:
                login_after_element = None

            # ログイン移行画面があった場合に「はい」をクリックする
            if login_after_element:
                self.logger.info(f"{self.__class__.__name__} ログイン移行画面が表示されました。")
                self.click_element.clickElement(by=self.const_element['LOGIN_TRANSFER_ID'], value=self.const_element['LOGIN_TRANSFER_VALUE'])
                self.random_sleep._random_sleep(2, 5)
            else:
                self.logger.info(f"{self.__class__.__name__} ログイン移行画面は表示されませんでした。")


            self.flow_asia_travel_first.single_process()

            self.flow_asia_travel_second.single_process()

            self.flow_ja_automakers.single_process()

            self.flow_trump.single_process()

            self.flow_china_ev.single_process()

            self.flow_korea.single_process()

            self.flow_asia_train.single_process()

            self.flow_ja_asia_entry.single_process()


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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# テスト実施

if __name__ == "__main__":

    test_flow = SingleProcess()
    # 引数入力

    url = "https://www.nna.jp/search?search_history=1747857031087&highlight=%E3%83%93%E3%82%B6"
    test_flow._single_process(url=url)
