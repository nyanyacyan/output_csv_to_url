# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from pdf2image import convert_from_path
import os


# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.errorHandlers import NetworkHandler
from method.base.utils.path import BaseToPath


# ----------------------------------------------------------------------------------
####################################################################################
# **********************************************************************************


class PDFtoImageConverter:
    def __init__(self):
        self.input_dir = '/Users/nyanyacyan/Desktop/project_file/utage_csv_to_gss/installer/src/method/inputData/PDF'
        self.output_dir = '/Users/nyanyacyan/Desktop/project_file/utage_csv_to_gss/installer/resultOutput/pdf_to_png'
        self.poppler_path = None
        os.makedirs(self.output_dir, exist_ok=True)

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.networkError = NetworkHandler()
        self.path = BaseToPath()


    #!###################################################################################
    # ✅ 行のcolumnからセルの列のアルファベットを出力

    def convert_all_pdfs(self):
        for pdf_file in os.listdir(self.input_dir):
            if pdf_file.lower().endswith(".pdf"):
                self._convert_single_pdf(pdf_file)

    #!###################################################################################
    # ----------------------------------------------------------------------------------

    def _convert_single_pdf(self, pdf_filename: str):
        pdf_path = os.path.join(self.input_dir, pdf_filename)
        print(f"🔄 Converting: {pdf_path}")
        images = convert_from_path(pdf_path, poppler_path=self.poppler_path)

        for i, image in enumerate(images):
            img_filename = f"{os.path.splitext(pdf_filename)[0]}.png"
            output_path = os.path.join(self.output_dir, img_filename)
            image.save(output_path, "PNG")
            print(f"✅ Saved: {output_path}")

    # ----------------------------------------------------------------------------------


if __name__ == "__main__":
    pdf_converter = PDFtoImageConverter()
    pdf_converter.convert_all_pdfs()
