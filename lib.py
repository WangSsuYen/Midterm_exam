import sqlite3, os, time, json


def connect_db(DB):
    pass


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
            conn.commit()
            conn.close()
            print(f"{DB}已經建立完成！")

        except sqlite3.Error as error :
            print(f"建立資料庫有個錯誤出現 ： {error} ")

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
                conn.commit()
                conn.close()
                print(f"成功匯入 {len(movies)} 筆電影資料。")
            except Exception as e:
                print(f"匯入電影資料時發生錯誤: {e}")


def search_movies(DB):
    if not os.path.exists(DB):
        print(f"資料庫檔案 {DB} 不存在，正在自動建立資料庫")
        create_table(DB)

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''SELECT * FROM movies ;''')
    datas = cur.fetchall()

    if not datas :
        print("查無資料。")
    else :
        print_value(datas)





def add_movie():
    pass

def modify_movie():
    pass

def delete_movies():
    pass

def export_movies():
    pass

def print_value(datas):
    print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<10}{'評分':{chr(12288)}<10}")
    print("-"*90)
    for data in datas :
        print(f"{data['title']:{chr(12288)}<10}{data['director']:{chr(12288)}<10}{data['genre']:{chr(12288)}<10}{data['year']:{chr(12288)}<10}{data['rating']:{chr(12288)}<10}")

