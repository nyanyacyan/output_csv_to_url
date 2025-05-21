# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
import sys

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.utils.popup import Popup

# ----------------------------------------------------------------------------------
####################################################################################
# **********************************************************************************


class CriticalHandler:
    def __init__(self):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.popup = Popup()

    #!###################################################################################
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, err_title: str, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.popup.popupCommentOnly(popupTitle=err_title, comment=error_comment)
        sys.exit(1)

    #!###################################################################################

# **********************************************************************************


class ErrorHandler:
    def __init__(self):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.popup = Popup()

    #!###################################################################################
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, err_title: str, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.popup.popupCommentOnly(popupTitle=err_title, comment=error_comment)
        sys.exit(1)

    #!###################################################################################

# **********************************************************************************


class WarningHandler:
    def __init__(self):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.popup = Popup()

    #!###################################################################################
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, err_title: str, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.popup.popupCommentOnly(popupTitle=err_title, comment=error_comment)
        sys.exit(1)

    #!###################################################################################

