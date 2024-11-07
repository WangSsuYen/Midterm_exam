import sqlite3, os
from lib import *

DB_path = "movies.db"
json_import_path = "movies.json"
json_export_path = "export.json"


while True :
    print("\n\n----- 電影管理系統 -----")
    print("1. 匯入電影資料檔")
    print("2. 查詢電影")
    print("3. 新增電影")
    print("4. 修改電影")
    print("5. 刪除電影")
    print("6. 匯出電影")
    print("7. 離開系統")
    print("------------------------")
    num = input("請選擇操作選項 (1-8) ： ")

    if num == "1" :
        import_movies(DB_path, json_import_path)

    elif num == "2" :
        search_movies(DB_path)

    elif num == "3" :
        add_movies(DB_path)

    elif num == "4" :
        modify_movies(DB_path)

    elif num == "5" :
        delete_movies(DB_path)

    elif num == "6" :
        export_movies(DB_path, json_export_path)

    elif num == "7" :
        break

    else :
        print(f"您輸入的( {num} )不是正確的數值，請重新輸入。")