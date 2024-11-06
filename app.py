import sqlite3, os
from lib import *

DB_path = "movies.db"
json_import_path = "movies.json"
json_export_path = "export.json"


while True :
    print("\n\n----- 電影管理系統 -----")
    print("1. 建立資料表結構")
    print("2. 匯入電影資料檔")
    print("3. 查詢電影")
    print("4. 新增電影")
    print("5. 修改電影")
    print("6. 刪除電影")
    print("7. 匯出電影")
    print("8. 離開系統")
    print("------------------------")
    num = input("請選擇操作選項 (1-8) ： ")

    if num == "1" :
        create_table(DB_path)

    elif num == "2" :
        list_rpt(DB_path, json_import_path)

    elif num == "3" :
        search_movies(DB_path)

    elif num == "4" :
        add_movie(DB_path)

    elif num == "5" :
        modify_movie(DB_path)

    elif num == "6" :
        delete_movies(DB_path)

    elif num == "7" :
        export_movies(DB_path, json_export_path)

    elif num == "8" :
        break

    else :
        print(f"您輸入的( {num} )不是正確的數值，請重新輸入。")