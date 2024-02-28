# from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import pandas as pd
from pywebio import session
from pywebio.pin import *
import jieba
import sqlite3
# https://blog.csdn.net/heianduck/article/details/121745458



def main():
    def callback_1():
        with use_scope("res", clear=True):
                results = pd.read_sql(f'select * from question1 q WHERE name LIKE "%{pin.search_content}%";', conn)
                for index, row in results.iterrows():
                    search_result = f"""
                        题目：{row["name"]}
                        题型：{row["type"]}
                        选项：{row["option"]}
                        答案：{row["answer"]}
                        -------------------------
                        """
                    put_text(search_result)
                


    # def callback_2():
    #     with use_scope("res", clear=True):
    #         results = pd.read_sql(f'select * from question1 q WHERE name LIKE "%{pin.search_content}%";', conn)
    #         for index, row in results.iterrows():
    #             search_result = f"""
    #                 题目：{row["name"]}
    #                 题型：{row["type"]}
    #                 选项：{row["option"]}
    #                 答案：{row["answer"]}
    #                 -------------------------
    #                 """
    #             print(search_result)
    #             keywords_list = jieba.cut(row["name"], cut_all=False)
    #             print(keywords_list)
    #             search_list = str(pin.search_content).split("，")
    #             ret = map(lambda s: s in keywords_list, search_list)
    #             if all(ret):
    #                 put_text(search_result)

    def callback_3():
        pin.search_content = ""
    put_input("search_content")
    put_buttons(["搜索"], lambda _: callback_1())
    put_buttons(["清空"], lambda _: callback_3())
    # put_buttons(["keywords search"], lambda _: callback_2())
    session.hold()


if __name__ == "__main__":
    conn = sqlite3.connect(r"D:\question_bank.db",check_same_thread=False)
    start_server(main, port=9999, host="0.0.0.0",debug=True)
    # s = "安全隐患"
    # results = pd.read_sql(f'select * from question1 q WHERE name LIKE "%{s}%";', conn)
    # print(results)

    
