# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2023/9/14 更新
# テストOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# import
import pathlib, sys
import os, platform
from datetime import datetime

# 自作モジュール
# import const
from method.base.utils.logger import Logger
from method.const_str import Dir, SubDir, Extension
from method.base.selenium.errorHandlers import AccessFileNotFoundError


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# 利用するメソッドがBaseだったときのクラス


class BaseToPath:
    def __init__(self):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.fileNotFoundError = AccessFileNotFoundError()
        self.currentDate = datetime.now().strftime("%y%m%d")
        self.fullCurrentDate = datetime.now().strftime("%y%m%d_%H%M%S")

    # ----------------------------------------------------------------------------------
    # logsFileを取得

    def toLogsPath(self, levelsUp: int = 4, subDirName: str = "logs"):
        resultOutputPath = self.getResultOutputPath(
            levelsUp=levelsUp, dirName=self.resultBox
        )
        logsPath = resultOutputPath / subDirName / self.currentDate
        self.isDirExists(path=logsPath)
        self.logger.debug(f"logsPath: {logsPath}")

        return logsPath

    # ----------------------------------------------------------------------------------
    # inputDataの中にあるFilePathを取得

    def getInputDataFilePath(self, fileName: str, levelsUp: int = 2):
        try:
            inputDataPath = self.getInputDataPath( levelsUp=levelsUp, dirName=self.inputBox )

            accessFilePath = inputDataPath / fileName
            self.logger.debug(f"{fileName} を発見: {accessFilePath}")

            return accessFilePath

        except Exception as e:
            self.fileNotFoundError.accessFileNotFoundError(fileName=fileName, e=e)

    # ----------------------------------------------------------------------------------
    # pickleFileを取得

    def getPickleFilePath(
        self, pklName: str, levelsUp: int = 4, subDirName: str = "pickles"
    ):
        picklesPath = self.toPicklesPath(
            levelsUp=levelsUp, dirName=self.resultBox, subDirName=subDirName
        )
        pickleFilePath = picklesPath / f"{pklName}.pkl"
        self.logger.debug(f"pickleFilePath: {pickleFilePath}")
        return pickleFilePath

    # ----------------------------------------------------------------------------------

    @property
    def currentDir(self):
        currentDirPath = pathlib.Path(__file__).resolve()
        return currentDirPath

    # ----------------------------------------------------------------------------------
    # resultOutputの大元の定義
    #! ディレクトリの変更があった場合にはレベルを調整

    def getResultOutputPath(self, levelsUp: int = 5, dirName: str = Dir.result.value):
        currentDirPath = self.currentDir
        self.logger.info(f"levelsUp の型: {type(levelsUp)}: {levelsUp}")

        # スタートが0で1つ上の階層にするため→levelsUpに１をいれたら１個上の階層にするため
        resultOutputPath = currentDirPath.parents[levelsUp - 1] / dirName
        self.logger.debug(f"{dirName}: {resultOutputPath}")
        return resultOutputPath

    # ----------------------------------------------------------------------------------

    def get_result_path_in_exe(self, levelsUp: int = 5, dirName: str = Dir.result.value):
        is_exe = self.is_exe()
        if is_exe:
            self.logger.warning("exeで実行されているため、デスクトップに保存します。")

            os_type = self.get_os()
            self.logger.debug(f"OSの種類: {os_type}")

            if os_type == "Windows":
                return self.get_result_dir_windows()

            elif os_type == "Mac":
                return self.get_result_dir_mac()

        currentDirPath = self.currentDir
        self.logger.info(f"levelsUp の型: {type(levelsUp)}: {levelsUp}")

        # スタートが0で1つ上の階層にするため→levelsUpに１をいれたら１個上の階層にするため
        resultOutputPath = currentDirPath.parents[levelsUp - 1] / dirName
        self.logger.debug(f"{dirName}: {resultOutputPath}")
        return resultOutputPath

    # ----------------------------------------------------------------------------------
    # exeで実行されているか確認

    def is_exe(self):
        if getattr(sys, 'frozen', False):
            self.logger.warning("exeで実行されている")
            return True

    # ----------------------------------------------------------------------------------
    # Macのパターン デスクトップに結果をresultOutputディレクトリを作成

    def get_result_dir_mac(self):
        desktop = pathlib.Path(os.environ["HOME"]) / "Desktop"
        result_dir = desktop / "resultOutput"
        result_dir.mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"Macの結果ディレクトリ: {result_dir}")
        return result_dir

    # ----------------------------------------------------------------------------------
    # windowsパターン デスクトップに結果をresultOutputディレクトリを作成

    def get_result_dir_windows(self):
        onedrive_path = pathlib.Path(os.environ.get("OneDrive", ""))
        if onedrive_path.exists():
            self.logger.warning("OneDriveが有効になっているため、デスクトップに保存します。")
            # OneDriveが有効な場合はデスクトップのパスを取得
            desktop = pathlib.Path(os.environ["USERPROFILE"]) / "OneDrive" / "デスクトップ"
        else:
            self.logger.info("OneDriveは有効ではありません。")
            desktop = pathlib.Path(os.environ["USERPROFILE"]) / "Desktop"
        result_dir = desktop / "resultOutput"
        result_dir.mkdir(parents=True, exist_ok=True)
        return result_dir

    # ----------------------------------------------------------------------------------
    # OS確認

    def get_os(self):
        os_name = platform.system()
        self.logger.debug(f"OS: {os_name}")

        if os_name == "Windows":
            self.logger.debug("Windows OSを検出しました。")
            return os_name
        elif os_name == "Darwin":
            self.logger.debug("Mac OSを検出しました。")
            return "Mac"
        else:
            self.logger.error("想定している OSではないため、処理を中断します。")
            raise NotImplementedError("想定している OSではないため、処理を中断")

    # ----------------------------------------------------------------------------------
    # inputDataへの大元の定義
    #! ディレクトリの変更があった場合にはレベルを調整
    def getInputDataPath(self, levelsUp: int = 3, dirName: str = Dir.input.value):
        currentDirPath = self.currentDir

        # スタートが0で1つ上の階層にするため→levelsUpに１をいれたら１個上の階層にするため
        inputDataPath = currentDirPath.parents[levelsUp - 1] / dirName
        self.logger.debug(f"{dirName}: {inputDataPath}")
        return inputDataPath

    # ----------------------------------------------------------------------------------
    # File名を付け足して書込時に拡張子を付け足す

    def getWriteFilePath(self, fileName: str):
        resultOutputPath = self.getResultOutputPath()
        filePath = resultOutputPath / fileName
        return filePath

    # ----------------------------------------------------------------------------------
    # ディレクトリがない可能性の箇所に貼る関数

    def isDirExists(self, path: pathlib):
        if not path.exists():
            # 親のディレクトリも作成、指定していたディレクトリが存在してもエラーを出さない
            path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"{path.name} がないため作成")
        else:
            self.logger.debug(f"{path.name} 発見")
        return path

    # ----------------------------------------------------------------------------------
    # ディレクトリがない可能性の箇所に貼る関数

    def isFileExists(self, path: pathlib):
        if not path.exists():
            path.touch()
            self.logger.info(f"{path.name} がないため作成")
        else:
            self.logger.debug(f"{path.name} 発見")
        return path

    # ---------------------------------------------------------------------------------
    # Input > File

    def getInputDataFilePath(self, fileName: str):
        inputDataPath = self.getInputDataPath()
        FilePath = inputDataPath / fileName
        self.logger.debug(f"FilePath: {FilePath}")
        return FilePath


    # ----------------------------------------------------------------------------------
    # Input > SubDir

    def getInputSubDirPath(self, subDirName: str):
        inputDataPath = self.getInputDataPath()
        dirPath = inputDataPath / subDirName
        self.logger.warning(f"dirPath: {dirPath}")
        self.logger.debug(f"dirPathの型: {type(dirPath)}")
        self.isDirExists(path=dirPath)
        return dirPath


    # ----------------------------------------------------------------------------------
    # Input > SubDir > File

    def getInputSubDirFilePath(self, subDirName: str, fileName: str, extension: str):
        inputDataPath = self.getInputDataPath()
        dirPath = inputDataPath / subDirName
        file = fileName + extension
        FilePath = dirPath / file
        self.logger.warning(f"FilePath: {FilePath}")
        self.logger.debug(f"FilePathの型: {type(FilePath)}")
        self.isDirExists(path=dirPath)
        self.logger.debug(f"FilePath: {FilePath}")
        return FilePath


    # ----------------------------------------------------------------------------------
    # Input > SubDir > extension_dir > File

    def _get_input_sub_sub_extension_file_path(self, sub_dir_name: str, file_name: str, extension: str, file_extension_bool: bool = False):
        inputDataPath = self.getInputDataPath()
        dirPath = inputDataPath / sub_dir_name / extension
        if file_extension_bool:
            file = file_name + extension
        else:
            file = file_name
        FilePath = dirPath / file
        self.logger.warning(f"FilePath: {FilePath}")
        self.logger.debug(f"FilePathの型: {type(FilePath)}")
        self.isDirExists(path=dirPath)
        self.logger.debug(f"FilePath: {FilePath}")
        return FilePath

    # ----------------------------------------------------------------------------------
    # Input > SubDir > extension_dir

    def _get_input_sub_sub_extension_folder(self, sub_dir_name: str, extension_folder_name: str):
        inputDataPath = self.getInputDataPath()
        dirPath = inputDataPath / sub_dir_name / extension_folder_name
        self.logger.warning(f"dirPath: {dirPath}")
        self.logger.debug(f"dirPathの型: {type(dirPath)}")
        return dirPath

    # ----------------------------------------------------------------------------------
    # Input > input_photo > SubDir

    def _get_input_photo_subdir_path(self, subDirName: str, input_photo: str = SubDir.INPUT_PHOTO.value):
        inputDataPath = self.getInputDataPath()
        dirPath = inputDataPath / input_photo / subDirName
        self.logger.warning(f"dirPath: {dirPath}")
        self.logger.debug(f"dirPathの型: {type(dirPath)}")
        self.isDirExists(path=dirPath)
        return dirPath

    # ----------------------------------------------------------------------------------
    # Input > input_photo > SubDir > SubSubDir

    def getInputPhotoDirPath(self, subDirName: str, subSubDirName: str, input_photo: str = SubDir.INPUT_PHOTO.value):
        inputDataPath = self.getInputDataPath()
        dirPath = inputDataPath / input_photo / subDirName / subSubDirName
        self.logger.warning(f"dirPath: {dirPath}")
        self.logger.debug(f"dirPathの型: {type(dirPath)}")
        self.isDirExists(path=dirPath)
        return dirPath

    # ----------------------------------------------------------------------------------
    # input_photo内にあるすべてのファイルのフルパスをリスト化する

    def _get_photos_all_path_list(self, photo_dir: str):
        dir_path = pathlib.Path(photo_dir)
        all_photos_all_path_list = [file for file in dir_path.rglob('*') if file.is_file()]
        self.logger.debug(f'all_photos_all_path_list: {all_photos_all_path_list}')
        return all_photos_all_path_list

    # ----------------------------------------------------------------------------------
    # Input > logo > SubDir

    def getInputLogoFilePath(self, fileName: str, subDirName: str=  SubDir.LOGO.value, extension: str= Extension.ICO.value):
        inputDataPath = self.getInputDataPath()
        dirPath = inputDataPath / subDirName
        file = fileName + extension
        FilePath = dirPath / file
        self.logger.warning(f"FilePath: {FilePath}")
        self.logger.debug(f"FilePathの型: {type(FilePath)}")
        self.isDirExists(path=dirPath)
        self.logger.debug(f"FilePath: {FilePath}")
        return FilePath


    # ----------------------------------------------------------------------------------
    # Input > driver > chrome > mac or win

    def _get_input_chromedriver_path(self):
        inputDataPath = self.getInputDataPath()
        chrome_dir_path = inputDataPath / "driver" / "chrome"

        # OSの名称確認
        os_name = platform.system()
        architecture = platform.architecture()[0]

        if os_name == "Windows":
            if architecture == "64bit":
                win_64_chrome_driver_path = chrome_dir_path / "chromedriver-win64" / "chromedriver.exe"
                self.isDirExists(path=win_64_chrome_driver_path)
                self.logger.debug(f'win-64のDriverを選択: {win_64_chrome_driver_path}\nOS: {os_name}, アーキテクチャ: {architecture}')
                return win_64_chrome_driver_path
            else:
                win_32_chrome_driver_path = chrome_dir_path / "chromedriver-win32" / "chromedriver.exe"
                self.isDirExists(path=win_32_chrome_driver_path)
                self.logger.debug(f'win-32のDriverを選択: {win_32_chrome_driver_path}\nOS: {os_name}, アーキテクチャ: {architecture}')
                return win_32_chrome_driver_path

        elif os_name == "Darwin":
            mac_chrome_driver_path = chrome_dir_path / "chromedriver-mac-arm64" / "chromedriver.exe"
            self.isDirExists(path=mac_chrome_driver_path)
            self.logger.debug(f'MacのDriverを選択: {mac_chrome_driver_path}\nOS: {os_name}, アーキテクチャ: {architecture}')
            return mac_chrome_driver_path


    # ----------------------------------------------------------------------------------
    # Input > driver > chrome > mac or win

    def _get_selenium_chromedriver_path(self):
        inputDataPath = self.getInputDataPath()
        chrome_dir_path = inputDataPath / "driver" / "chrome" / "cache"
        self.isDirExists(path=chrome_dir_path)
        self.logger.debug(f'MacのDriverを選択: {chrome_dir_path}')
        return str(chrome_dir_path)


    # ----------------------------------------------------------------------------------
    # Input > chrome > file

    def _get_chrome_path(self, file_name: str):
        inputDataPath = self.getInputDataPath()
        chrome_dir_path = inputDataPath / "chrome" / file_name
        self.isDirExists(path=chrome_dir_path)
        self.logger.debug(f'拡張機能のあるPath: {chrome_dir_path}')
        return str(chrome_dir_path)


    # ----------------------------------------------------------------------------------
    # Input > secret_key > file

    def _get_secret_key_path(self, file_name: str):
        inputDataPath = self.getInputDataPath()
        chrome_dir_path = inputDataPath / "secret_key" / file_name
        self.isDirExists(path=chrome_dir_path)
        self.logger.debug(f'MacのDriverを選択: {chrome_dir_path}')
        return str(chrome_dir_path)


    # ----------------------------------------------------------------------------------
    #     # Result > File

    def getResultFilePath(self, fileName: str):
        resultOutputPath = self.getResultOutputPath()
        FilePath = resultOutputPath / fileName
        self.isDirExists(path=FilePath)
        self.logger.debug(f"FilePath: {FilePath}")
        return FilePath

    # ----------------------------------------------------------------------------------
    # Result > SubDir > File

    def getResultSubDirFilePath(self, subDirName: str, fileName: str, extension: str):
        resultOutputPath = self.getResultOutputPath()
        dirPath = resultOutputPath / subDirName
        file = fileName + extension
        FilePath = dirPath / file
        self.logger.warning(f"FilePath: {FilePath}")
        self.logger.debug(f"FilePathの型: {type(FilePath)}")
        self.isDirExists(path=dirPath)
        self.logger.debug(f"FilePath: {FilePath}")
        return FilePath

    # ----------------------------------------------------------------------------------
    # Result > SubDir > date > file

    def result_sub_date_file_path(self, subDirName: str, fileName: str, extension: str):
        resultOutputPath = self.getResultOutputPath()
        dirPath = resultOutputPath / subDirName / self.currentDate
        file = fileName + extension
        FilePath = dirPath / file
        self.logger.warning(f"FilePath: {FilePath}")
        self.logger.debug(f"FilePathの型: {type(FilePath)}")
        self.isDirExists(path=dirPath)
        self.logger.debug(f"FilePath: {FilePath}")
        return FilePath

    # ----------------------------------------------------------------------------------
    # Result > account_name > date > SubDir > file

    def result_ac_date_sub_path(self, account_dir_name: str, sub_dir_name: str, file_name: str, extension: str):
        result_output_path = self.getResultOutputPath()
        dir_path = result_output_path / account_dir_name / self.currentDate / sub_dir_name
        self.logger.debug(f'dir_path: {dir_path}')
        file = file_name + extension
        file_path = dir_path / file
        self.logger.warning(f"file_path: {file_path}")
        self.logger.debug(f"file_pathの型: {type(file_path)}")
        self.isDirExists(path=dir_path)
        self.logger.debug(f"file_path: {file_path}")
        return file_path

    # ----------------------------------------------------------------------------------
    # Result > account_name > date > SubDir > file

    def result_ac_date_sub_path_two(self, account_dir_name: str, sub_dir_name: str, file_name: str):
        result_output_path = self.getResultOutputPath()
        dir_path = result_output_path / account_dir_name / self.currentDate / sub_dir_name
        file_path = dir_path / file_name
        self.logger.warning(f"file_path: {file_path}")
        self.logger.debug(f"file_pathの型: {type(file_path)}")
        self.isDirExists(path=dir_path)
        self.logger.debug(f"file_path: {file_path}")
        return file_path

    # ----------------------------------------------------------------------------------
    # Result > SubDir > FileName0101.txt

    def getResultSubDirDateFilePath(
        self, subDirName: str, fileName: str, extension: str
    ):
        resultOutputPath = self.getResultOutputPath()
        dirPath = resultOutputPath / subDirName
        file = fileName + self.fullCurrentDate + extension
        FilePath = dirPath / file
        self.logger.warning(f"FilePath: {FilePath}")
        self.logger.debug(f"FilePathの型: {type(FilePath)}")
        self.isDirExists(path=dirPath)
        self.logger.debug(f"FilePath: {FilePath}")
        return FilePath

    # ----------------------------------------------------------------------------------
    # Result > SubDir > 0101.db

    def getResultDBDirPath( self, subDirName: str = SubDir.DBSubDir.value, ):
        resultOutputPath = self.getResultOutputPath()

        dirPath = resultOutputPath / subDirName
        self.isDirExists(path=dirPath)
        self.logger.debug(f"dirPath: {dirPath}")

        return dirPath

    # ----------------------------------------------------------------------------------
    # Result > SubDir > DB > BuckUp

    def getResultDBBackUpDirPath(self, subDirName: str = SubDir.BUCK_UP.value):
        db_Path = self.getResultDBDirPath()
        dirPath = db_Path / subDirName
        self.isDirExists(path=dirPath)
        self.logger.debug(f"dirPath: {dirPath}")

        return dirPath

    # ----------------------------------------------------------------------------------
    # Result > SubDir > DB > db_file_name.db

    def _db_path(self, db_file_name: str, extension: str = Extension.DB.value):
        db_dir_path = self.getResultDBDirPath()
        self.logger.debug(f"db_dir_path: {db_dir_path}")
        dbFilePath = db_dir_path / f"{db_file_name}{extension}"
        self.logger.debug(f"dbFilePath: {dbFilePath}")
        return dbFilePath

    # ----------------------------------------------------------------------------------
    # Result > SubDir > DB > Buckup > db_file_name0101.db

    def _db_backup_path(self, db_file_name: str, extension: str = Extension.DB.value):
        db_dir_path = self.getResultDBBackUpDirPath()
        self.logger.debug(f"db_dir_path: {db_dir_path}")
        dbFilePath = db_dir_path / f"{db_file_name}{self.currentDate}{extension}"
        self.logger.debug(f"dbFilePath: {dbFilePath}")
        return dbFilePath

    # ----------------------------------------------------------------------------------
    # resultOutput > 0101 > file_name

    def writeFileDateNamePath(self, extension: str, subDirName: str):
        resultOutputPath = self.getResultOutputPath()
        fileFullPath = (
            resultOutputPath
            / subDirName
            / self.currentDate
            / f"{self.currentDate}{extension}"
        )
        self.isDirExists(path=fileFullPath)
        self.logger.debug(f"fileFullPath: {fileFullPath}")
        return fileFullPath

    # ----------------------------------------------------------------------------------
    # resultOutput > 0101 > 0101.txt

    def writeFileDateNamePath(self, extension: str, subDirName: str):
        resultOutputPath = self.getResultOutputPath()
        fileFullPath = (
            resultOutputPath
            / subDirName
            / self.currentDate
            / f"{self.currentDate}{extension}"
        )
        self.isDirExists(path=fileFullPath)
        self.logger.debug(f"fileFullPath: {fileFullPath}")
        return fileFullPath

    # ----------------------------------------------------------------------------------
    # resultOutput > 0101 > fileName.txt

    def writeFileNamePath(self, subDirName: str, fileName: str, extension: str):
        resultOutputPath = self.getResultOutputPath()
        fileFullPath = (
            resultOutputPath / subDirName / self.currentDate / f"{fileName}{extension}"
        )
        self.isDirExists(path=fileFullPath)
        self.logger.debug(f"fileFullPath: {fileFullPath}")
        return fileFullPath

    # ----------------------------------------------------------------------------------
    # resultOutput > 0101 > 0101.pkl

    def writePicklesFileDateNamePath(
        self,
        extension: str = Extension.pickle.value,
        subDirName: str = SubDir.pickles.value,
    ):
        resultOutputPath = self.getResultOutputPath()
        pickleFullPath = (
            resultOutputPath
            / subDirName
            / self.currentDate
            / f"{self.currentDate}{extension}"
        )
        self.isDirExists(path=pickleFullPath)
        self.logger.debug(f"pickleFullPath: {pickleFullPath}")
        return pickleFullPath

    # ----------------------------------------------------------------------------------
    # resultOutput > 0101 > 0101.txt

    def writeCookiesFileDateNamePath(
        self,
        extension: str = Extension.cookie.value,
        subDirName: str = SubDir.cookies.value,
    ):
        resultOutputPath = self.getResultOutputPath()
        cookieFullPath = (
            resultOutputPath
            / subDirName
            / self.currentDate
            / f"{self.currentDate}{extension}"
        )
        self.isDirExists(path=cookieFullPath)
        self.logger.debug(f"cookieFullPath: {cookieFullPath}")
        return cookieFullPath

    # ----------------------------------------------------------------------------------
    # resultOutput > 0101.pkl

    def getPickleDirPath(self, subDirName: str = SubDir.pickles.value):
        resultOutputPath = self.getResultOutputPath()
        return os.path.join(resultOutputPath, subDirName)

    # ----------------------------------------------------------------------------------
    # resultOutput > 0101cookie.pkl

    def getCookieDirPath(self, subDirName: str = SubDir.cookies.value):
        resultOutputPath = self.getResultOutputPath()
        return os.path.join(resultOutputPath, subDirName)


# ----------------------------------------------------------------------------------
