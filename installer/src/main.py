# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/LGRAM_auto_processer/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

# flow
from method.flow import SingleProcess
from tkinter import *
from tkinter import messagebox, ttk

from method.const_element import GUIInfo

from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------------------------------------------------
# **********************************************************************************

def submit(url: str, keyword: str):
    main_flow = SingleProcess()
    main_flow._single_process(url=url)
    messagebox.showinfo("CSV出力完了", "「resultOutput」の中にあるデータをご確認ください")

# **********************************************************************************

if __name__ == "__main__":

    title = GUIInfo.OUTPUT_CSV.value["WINDOW_TITLE"]
    window_width = GUIInfo.OUTPUT_CSV.value["WINDOW_WIDTH"]
    window_height = GUIInfo.OUTPUT_CSV.value["WINDOW_HEIGHT"]
    window_size = f"{window_width}x{window_height}"

    # Window作成
    window = Tk()
    window.title(title)
    window.geometry(window_size)

    # 検索ワードの大枠のフレーム作成
    search_url_frame = ttk.Frame(window, padding=(10, 20, 10, 10))
    search_url_frame.grid(row=0, column=0, sticky=W)

    #search_urlの説明欄（左側）
    # padding=(10, 10)この部分がラベルの余白を設定。　左側「左右」、右側「上下」の余白
    search_url_label = ttk.Label(search_url_frame, text="対象URL", width=8, padding=(10, 10))
    search_url_label.grid(row=0, column=0)

    #search_urlの入力ラベル（真ん中）
    search_url_entry = ttk.Entry(search_url_frame, width=48)
    search_url_entry.grid(row=0, column=1, padx=(10, 0))

    # レコメンド入力欄 大枠フレーム作成
    keyword_frame = ttk.Frame(window, padding=(10, 10, 20, 10))
    keyword_frame.grid(row=1, column=0, sticky=W)

    #keyword 説明欄（左側）
    # padding=(10, 10)この部分がラベルの余白を設定。左側「左右」、右側「上下」の余白
    keyword_label = ttk.Label(keyword_frame, text="キーワード", width=8, padding=(10, 10))
    keyword_label.grid(row=1, column=0)

    #keyword 入力ラベル（真ん中）
    keyword_entry = ttk.Entry(keyword_frame, width=48)
    keyword_entry.grid(row=1, column=1, padx=(10, 0))

    # Runningフレーム作成
    running_frame = ttk.Frame(window, padding=(50, 20, 10, 0))
    running_frame.grid(row=4, column=0, )

    # runningボタン作成
    input_url = search_url_entry.get()
    input_keyword = keyword_entry.get()

    submit_button = ttk.Button(running_frame, text="CSV出力開始", command=lambda: submit(url=input_url, keyword=input_keyword))
    submit_button.grid(row=3, column=0, padx=40)

    # cancelボタン作成
    cancel_button = ttk.Button(running_frame, text="閉じる", command=window.destroy)
    cancel_button.grid(row=3, column=1, padx=40)

    # error_messageフレーム作成
    error_frame = ttk.Frame(window, padding=10, width=10)
    error_frame.grid(row=5, column=0)

    # error_messageラベル作成
    error_message_label = ttk.Label(error_frame, text="", foreground="red", wraplength=480, font=("Helvetica", 10))
    error_message_label.grid(row=5, column=0)

    window.mainloop()

# ----------------------------------------------------------------------------------
