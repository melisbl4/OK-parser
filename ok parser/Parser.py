from selenium import webdriver as wd
import sqlite3
import OKWorker as ok
import SQLWriter as db

conn = sqlite3.connect("okpars.db")
cur = conn.cursor()
db.createDB(conn, cur)

browser = wd.Chrome()
browser.maximize_window()
ok.logIn(browser)

id_post = 1
id_comment = 1
id_media = 1
id_user = 1
# group = [id,  group_link,                          group_name,                                    first_post_link]
groups = [[1,  "https://ok.ru/oklive",              "Одноклассники. OK Live",                      "https://ok.ru/oklive/topic/131090342767520"],
          [2,  "https://ok.ru/okmusic",             "Музыка в ОК",                                 "https://ok.ru/okmusic/topic/156186647221144"],
          [3,  "https://ok.ru/nationalprojectsru",  "Национальные проекты России",                 "https://ok.ru/nationalprojectsru/topic/155848698098661"],
          [4,  "https://ok.ru/gazprom",             "Газпром",                                     "https://ok.ru/gazprom/topic/155389701914071"],
          [5,  "https://ok.ru/rostelecom.official", "Ростелеком",                                  "https://ok.ru/rostelecom.official/topic/156572657016177"],
          [6,  "https://ok.ru/vtb",                 "ВТБ",                                         "https://ok.ru/vtb/topic/151784786552195"],
          [7,  "https://ok.ru/ok",                  "Всё ОК!",                                     "https://ok.ru/ok/topic/155581345751259"],
          [8,  "https://ok.ru/ria",                 "РИА Новости",                                 "https://ok.ru/ria/topic/156596360539541"],
          [9,  "https://ok.ru/borsch1",             "Борщ",                                        "https://ok.ru/borsch1/topic/156109473734746"],
          [10, "https://ok.ru/maximum",             "Радио MAXIMUM",                               "https://ok.ru/maximum/topic/156219791047659"],
          [11, "https://ok.ru/s7airlines",          "S7 Airlines",                                 "https://ok.ru/s7airlines/topic/156915038718739"],
          [12, "https://ok.ru/tele2",               "Tele2 Россия",                                "https://ok.ru/tele2/topic/159097571313664"],
          [13, "https://ok.ru/stoloto",             "Столото. Государственные лотереи",            "https://ok.ru/stoloto/topic/156719786293494"],
          [14, "https://ok.ru/topfactor23",         "Топ Фактор. История, наука, факты, животные", "https://ok.ru/topfactor23/topic/156721744829803"],
          [15, "https://ok.ru/dtrad43",             "Деревенские Традиции",                        "https://ok.ru/dtrad43/topic/155712825023398"],
          [16, "https://ok.ru/sber",                "Сбер",                                        "https://ok.ru/sber/topic/156440160884949"]]

for group in groups:
    id_post, id_media, id_comment, id_user = ok.parsGroup(conn, cur, browser, group, id_post, id_media, id_comment, id_user)