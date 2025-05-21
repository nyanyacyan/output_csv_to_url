# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/LGRAM_auto_processer/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

# flow
from method.flow import SingleProcess
from method.base.utils.logger import Logger
from tkinter import *
from tkinter import messagebox, ttk

from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------------------------------------------------
# **********************************************************************************

def main():
    main_flow = SingleProcess()
    main_flow._single_process()

# **********************************************************************************

if __name__ == "__main__":

    # Window作成
    window = Tk()
    window.title("google_map_api_tool")
    window.geometry('445x260')


    # 検索ワードの大枠のフレーム作成
    search_word_frame = ttk.Frame(window, padding=(10, 20, 0, 10))
    search_word_frame.grid(row=0, column=0, sticky=W)

    #search_wordの説明欄（左側）
    # padding=(10, 10)この部分がラベルの余白を設定。　左側「左右」、右側「上下」の余白
    search_word_label = ttk.Label(search_word_frame, text="検索ワード", width=8, padding=(10, 10))
    search_word_label.grid(row=0, column=0)

    #search_wordの入力ラベル（真ん中）
    search_word_entry = ttk.Entry(search_word_frame, width=25)
    search_word_entry.grid(row=0, column=1, padx=(10, 0))

    # ボタンなし


    # レコメンド入力欄 大枠フレーム作成
    recommend_frame = ttk.Frame(window, padding=(10, 20, 0, 10))
    recommend_frame.grid(row=1, column=0, sticky=W)

    #recommend 説明欄（左側）
    # padding=(10, 10)この部分がラベルの余白を設定。左側「左右」、右側「上下」の余白
    recommend_label = ttk.Label(recommend_frame, text="レコメンド", width=8, padding=(10, 10))
    recommend_label.grid(row=1, column=0)

    #recommend 入力ラベル（真ん中）
    recommend_entry = ttk.Entry(recommend_frame, width=25)
    recommend_entry.grid(row=1, column=1, padx=(10, 0))

    # ボタンなし


    # error_messageフレーム作成
    error_frame = ttk.Frame(window, padding=10, width=10)
    error_frame.grid(row=3, column=0)

    # error_messageラベル作成
    error_message_label = ttk.Label(error_frame, text="", foreground="red", wraplength=480, font=("Helvetica", 10))
    error_message_label.grid(row=3, column=0)



    # Runningフレーム作成
    running_frame = ttk.Frame(window, padding=(60, 15, 10, 0))
    running_frame.grid(row=5, column=0, )

    # runningボタン作成
    submit_button = ttk.Button(running_frame, text="html 生成 開始", command=submit)
    submit_button.grid(row=4, column=0, padx=20)

    # cancelボタン作成
    cancel_button = ttk.Button(running_frame, text="閉じる", command=quit)
    cancel_button.grid(row=4, column=1, padx=20)

    window.mainloop()

# ----------------------------------------------------------------------------------
