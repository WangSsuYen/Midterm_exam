import sqlite3, os, time, json

# 創建資料表單方法
def create_table(DB):
    if os.path.exists(DB):
        print(f"資料庫: {DB} 已存在。")

    else :
        print("資料表單建立中......")
        time.sleep(1)
        try :
            # 連接到 SQLite 資料庫（如果資料庫不存在，則會創建它）
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS movies(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        director TEXT NOT NULL,
                        genre TEXT NOT NULL,
                        year INTEGER NOT NULL,
                        rating REAL);''')
            # 提交變更並關閉資料庫連線

            print(f"{DB}已經建立完成！")

        except sqlite3.Error as error :
            print(f"建立資料庫有個錯誤出現 ： {error} ")

        finally :
            conn.commit()
            conn.close()

#匯入電影資料檔 (JSON 格式)
def import_movies(DB, jsons):
    if not os.path.exists(DB):
        print(f"資料庫檔案 {DB} 不存在，正在自動建立資料庫")
        create_table(DB)

    if not os.path.exists(jsons):
        print(f"無法找到 JSON 檔案: {jsons}")

    else :
        with open(jsons, 'r', encoding='utf-8') as file:
            try:
                movies = json.load(file)
                conn = sqlite3.connect(DB)
                cur = conn.cursor()
                for movie in movies:
                    # 假設每筆資料都有 title, director, genre, year 和 rating 欄位
                    cur.execute('''
                        INSERT INTO movies (title, director, genre, year, rating)VALUES (?, ?, ?, ?, ?)''',
                        (movie['title'], movie['director'], movie['genre'], movie['year'], movie.get('rating')))

                print(f"成功匯入 {len(movies)} 筆電影資料。")
            except Exception as e:
                print(f"匯入電影資料時發生錯誤: {e}")
            finally :
                conn.commit()
                conn.close()
                file.close()

# 查詢電影方法
def search_movies(DB):
    if not os.path.exists(DB):
        print(f"資料庫檔案 {DB} 不存在，正在自動建立資料庫")
        create_table(DB)

    search_all = input("查詢全部電影嗎？(y/n) ： ")
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if search_all.lower() == "y":
        cur.execute('''SELECT * FROM movies ;''')
        datas = cur.fetchall()
        if not datas :
            print("查無資料。")
        else :
            print_value(datas)

    elif search_all.lower() == "n":
        search_name = input("請輸入電影名稱 : ")
        cur.execute('''SELECT * FROM movies WHERE title LIKE ?;''', ('%' + search_name + '%',))
        datas = cur.fetchall()
        if not datas :
            print("查無資料。")
        else :
            print_value(datas)

    conn.close()



# 新增電影方法
def add_movies(DB):
    if not os.path.exists(DB):
        print(f"資料庫檔案 {DB} 不存在，正在自動建立資料庫")
        create_table(DB)

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # 抓取欄位名稱
    field_map = {
            'title': "電影名稱",
            'director': "導演",
            'genre': "類別",
            'year': "年份",
            'rating': "評分(1.0-10.0)"
        }

    print("請依照以下欄位名稱輸入電影資料：")
    data = {}  # 儲存使用者輸入的資料
    try:
        for col, val in field_map.items():
            while True:  # 進行一個循環，直到使用者提供有效資料
                user_input = input(f"請輸入 {val} : ").strip()  # 去除首尾空白
                if user_input == "":  # 檢查是否輸入空值
                    print(f"{val} 不能為空，請重新輸入。")
                else:
                    # 檢查電影名稱是否已存在
                    if col == 'title':
                        cur.execute("SELECT COUNT(*) FROM movies WHERE title = ?", (user_input,))
                        count = cur.fetchone()[0]
                        if count > 0:
                            print(f"電影名稱 '{user_input}' 已經存在，請輸入其他名稱。")
                            continue  # 重新要求輸入電影名稱

                    # 檢查評分範圍
                    if col == 'rating':
                        try:
                            rating = float(user_input)
                            if rating < 1.0 or rating > 10.0:
                                print("評分必須在 1.0 到 10.0 之間，請重新輸入。")
                                continue
                            data[col] = rating
                        except ValueError:
                            print("評分必須是數字，請重新輸入。")
                            continue
                    else:
                        data[col] = user_input
                    break  # 跳出循環，繼續處理下個欄位

        placeholders = ', '.join(['?'] * len(data))  # 為 SQL 語句準備佔位符
        sql = f"INSERT INTO movies ({', '.join(data.keys())}) VALUES ({placeholders})"
        cur.execute(sql, tuple(data.values()))
        conn.commit()

        print("電影資料已成功新增！")

    except sqlite3.Error as e:
        print(f"資料庫操作錯誤: {e}")
    except Exception as e:
        print(f"發生未知錯誤: {e}")
    finally:
        conn.close()  # 確保資料庫連線關閉



def modify_movies(DB):
    if not os.path.exists(DB):
        print(f"資料庫檔案 {DB} 不存在，正在自動建立資料庫")
        create_table(DB)

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    modity_movie = input("請輸入要修改的電影名稱 ： ")
    cur.execute('''SELECT * FROM movies WHERE title LIKE ?;''', ('%' + modity_movie + '%',))
    datas = cur.fetchall()
    if not datas :
        print('查無資料。')
    else :
        print_value(datas)
        # 字典定義
        field_map = {
            'title': "電影名稱",
            'director': "導演",
            'genre': "類別",
            'year': "年份",
            'rating': "評分(1.0-10.0)"
        }
        # 讓使用者輸入新的資料
        updated_data = {}
        for col, val in field_map.items():
            # 請使用者輸入新的資料，若按Enter則保持原值
            new_value = input(f"請輸入新的 {val} (若不修改請直接按 Enter): ").strip()

            # 如果使用者輸入了新值，則更新
            if new_value:
                updated_data[col] = new_value
            else:
                # 若不輸入則保留原來的值
                updated_data[col] = datas[0][col]

        # 更新資料庫
        try:
            cur.execute('''UPDATE movies SET
                            title = ?, director = ?, genre = ?, year = ?, rating = ?
                            WHERE id = ?;''',
                        (updated_data['title'], updated_data['director'], updated_data['genre'],
                         updated_data['year'], updated_data['rating'], datas[0]['id']))

            conn.commit()
            print("資料已修改")
        except sqlite3.Error as error:
            print(f"修改資料時發生錯誤: {error}")

    conn.close()




# 刪除電影方法
def delete_movies(DB):
    if not os.path.exists(DB):
        print(f"資料庫檔案 {DB} 不存在，正在自動建立資料庫")
        create_table(DB)

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    delete_data = input("刪除全部電影嗎？(y/n) ： ")
    if delete_data.lower() == "y" :
        cur.execute("DELETE FROM movies ;")
        print("已刪除全部電影。")

    elif delete_data.lower() == "n" :
        delete_movie = input("請輸入要刪除的電影名稱 : ")
        cur.execute('''SELECT * FROM movies WHERE title LIKE ?;''', ('%' + delete_movie + '%',))
        datas = cur.fetchall()
        if not datas :
            print("查無資料。")
        else :
            print_value(datas)
            correct_react = input("確定要刪除此電影嗎 ? (y/n) ： ")
            if correct_react.lower() == "y" :
                cur.execute("DELETE FROM movies WHERE title LIKE ?;", ('%' + delete_movie + '%',))
                print("已刪除電影。")
            else :
                print("想清楚再來吧!")
    else :
        print("錯誤選項，請思考清楚再來。")
    conn.commit()
    conn.close()


# 匯出電影資料到 JSON 檔案
def export_movies(DB, jsons):
    if not os.path.exists(DB):
        print(f"資料庫檔案 {DB} 不存在，無法匯出資料")
        return

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row  # 讓資料查詢結果變成字典形式
    cur = conn.cursor()

    try:
        # 查詢所有電影資料
        cur.execute("SELECT * FROM movies;")
        datas = cur.fetchall()

        if not datas:
            print("資料庫中沒有電影資料，無法匯出。")
        else:
            # 將資料轉換為字典格式的列表
            movie_list = []
            for movie in datas:
                movie_data = {
                    "id": movie["id"],
                    "title": movie["title"],
                    "director": movie["director"],
                    "genre": movie["genre"],
                    "year": movie["year"],
                    "rating": movie["rating"]
                }
                movie_list.append(movie_data)

            # 將電影資料寫入 JSON 檔案
            with open(jsons, 'w', encoding='utf-8') as json_file:
                json.dump(movie_list, json_file, ensure_ascii=False, indent=4)

            print(f"成功匯出 {len(movie_list)} 筆電影資料到 {jsons}。")

    except sqlite3.Error as error:
        print(f"資料庫錯誤: {error}")

    finally:
        conn.close()  # 關閉資料庫連線

# 印出電影明細
def print_value(datas):
    print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<10}{'評分':{chr(12288)}<10}")
    print("-"*90)
    for data in datas :
        print(f"{data['title']:{chr(12288)}<10}{data['director']:{chr(12288)}<10}{data['genre']:{chr(12288)}<10}{data['year']:{chr(12288)}<10}{data['rating']:{chr(12288)}<10}")

