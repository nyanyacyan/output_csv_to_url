# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/ccx_csv_to_drive/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/output_csv_to_url/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from datetime import datetime
from selenium.webdriver.chrome.webdriver import WebDriver

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.selenium.get_element import GetElement
from method.base.decorators.decorators import Decorators
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.utils.popup import Popup
from method.base.selenium.click_element import ClickElement
from method.base.utils.fileWrite import FileWrite


# const
from method.const_element import ( CsvInfo, LoginInfo, ErrCommentInfo, PopUpComment, Element, KeyWordInfo)

# flow

deco = Decorators()

# ----------------------------------------------------------------------------------
#! 日系製造業のアジア進出
# **********************************************************************************
# 一連の流れ


class FlowJaAsiaEntry:
    """日系製造業のアジア進出を取得するクラス"""
    def __init__(self, chrome: WebDriver):
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        self.timestamp = datetime.now()
        self.timestamp_two = self.timestamp.strftime("%Y-%m-%d_%H-%M")
        self.date_only_stamp = self.timestamp.date().strftime("%m月%d日")

        # Chrome → Flowにて渡す
        self.chrome = chrome

        # const
        self.const_login_info = LoginInfo.OUTPUT_CSV.value
        self.const_element = Element.OUTPUT_CSV.value
        self.const_err_cmt_dict = ErrCommentInfo.OUTPUT_CSV.value
        self.popup_cmt = PopUpComment.OUTPUT_CSV.value
        self.const_csv_info = CsvInfo.OUTPUT_CSV.value

        # キーワード
        self.keyword = KeyWordInfo.TRUMP.value

        # インスタンス
        self.login = SingleSiteIDLogin(chrome=self.chrome)
        self.random_sleep = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.selenium = SeleniumBasicOperations(chrome=self.chrome)
        self.popup = Popup()
        self.click_element = ClickElement(chrome=self.chrome)
        self.file_write = FileWrite()

    # **********************************************************************************
    # ----------------------------------------------------------------------------------

    def single_process(self):
        """各プロセスを実行する"""
        try:
            self.logger.info(f"{self.__class__.__name__} 開始")

            home_url = self.const_login_info['HOME_URL']
            self.logger.debug(f"HomeUrl: {home_url}")

            # 新しいページでurlを開く
            self.get_element._open_new_page(url=home_url)
            self.random_sleep._random_sleep(2, 5)

            # 詳細検索をクリック
            self.click_element.clickElement(value=self.const_element['DETAIL_SEARCH_VALUE'])
            self.random_sleep._random_sleep(2, 5)

            # キーワードの入力
            self.get_element.clickClearInput(value=self.const_element['KEYWORD_VALUE'], inputText=self.keyword['TRUMP'])
            self.random_sleep._random_sleep(2, 5)

            # TODO 期間をクリック
            self.click_element.clickElement(value=self.const_element['DETAIL_SEARCH_VALUE'])
            self.random_sleep._random_sleep(2, 5)

            # TODO 1日以内をクリック
            self.click_element.clickElement(value=self.const_element['DETAIL_SEARCH_VALUE'])
            self.random_sleep._random_sleep(2, 5)

            # TODO 国をクリック
            self.click_element.clickElement(value=self.const_element['DETAIL_SEARCH_VALUE'])
            self.random_sleep._random_sleep(2, 5)

            # TODO 国を選択するためにクリック→keyの数を数えてその分繰り返し実施

            # TODO 業種をクリック
            self.click_element.clickElement(value=self.const_element['DETAIL_SEARCH_VALUE'])
            self.random_sleep._random_sleep(2, 5)

            # TODO 各業種を選択するためにクリック→keyの数を数えてその分繰り返し実施

            # TODO 検索対象をクリック
            self.click_element.clickElement(value=self.const_element['DETAIL_SEARCH_VALUE'])
            self.random_sleep._random_sleep(2, 5)

            # TODO 検索対象を選択するためにクリック→keyの数を数えてその分繰り返し実施

            # TODO 検索ボタンをクリック
            self.click_element.clickElement(value=self.const_element['DETAIL_SEARCH_VALUE'])
            self.random_sleep._random_sleep(2, 5)

            # 要素のリスト取得（テーブルの取得）
            main_element = self.get_element.getElement(by=self.const_element['BY_MAIN'], value=self.const_element['VALUE_MAIN'])
            self.logger.info(f"main_element: {main_element}")

            ul_elements = self.get_element.filterElement(parentElement=main_element, by=self.const_element['by_0'], value=self.const_element['value_0'])
            self.logger.info(f"ul_elements: {ul_elements}")

            li_elements = self.get_element.filterElements(parentElement=ul_elements, by=self.const_element['by_1'], value=self.const_element['value_1'])
            self.logger.info(f"li_elements: {li_elements} 要素数: {len(li_elements)}つ")

            csv_list = []
            # 要素１つずつにアクセス
            for e in li_elements:
                self.logger.info(f"element: {e}")
                # country_name_elements = self.get_element.filterElements(parentElement=e, value=self.const_element['value_2'])
                # self.logger.info(f"country_name_elements: {country_name_elements} 要素数: {len(country_name_elements)}つ")

                # 国名が書かれている要素を取得
                country_name_element = self.get_element.filterElement(parentElement=e, value=self.const_element['value_2'])

                # 国名,抽出
                if country_name_element is None:
                    self.logger.error(f"{self.__class__.__name__} 国名の要素が見つかりませんでした。")
                    continue

                country_name = country_name_element.text
                self.logger.info(f"国名: {country_name}")

                # URLが書かれている要素を取得
                url_elements = self.get_element.filterElements(parentElement=e, by=self.const_element['by_4'], value=self.const_element['value_4'])
                self.logger.info(f"url_elements: {url_elements} 要素数: {len(url_elements)}つ")

                url_str = url_elements[1].get_attribute("href")
                self.logger.info(f"url: {url_str}")

                title_str = url_elements[1].text
                self.logger.info(f"記事名: {title_str}")

                # リストに追加
                csv_list.append([country_name, title_str, url_str])

            self.logger.info(f"csv_list: {csv_list}")

            # csvファイルに書き込めるように修正
            file_name = f"nna_{self.timestamp_two}"

            # csvファイルに書き込み
            self.file_write.write_cst_to_list(col_names=self.const_csv_info['COL_NAME'], data=csv_list, fileName=file_name)


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

    test_flow = FlowJaAsiaEntry()
    # 引数入力

    url = "https://www.nna.jp/search?search_history=1747857031087&highlight=%E3%83%93%E3%82%B6"
    test_flow.single_process(url=url)
