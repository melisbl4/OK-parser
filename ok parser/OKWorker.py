from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from datetime import date, timedelta
import SQLWriter as db


def dateFormat(date_):
    s = list(date_.split())
    if len(s) == 1:
        return date.today()
    elif len(s) == 2 and s[0] == "вчера":
        return date.today() - timedelta(days=1)
    else:
        s[0] = int(s[0])
        if s[1] == "янв":
            s[1] = 1
        elif s[1] == "фев":
            s[1] = 2
        elif s[1] == "марта":
            s[1] = 3
        elif s[1] == "апр":
            s[1] = 4
        elif s[1] == "мая":
            s[1] = 5
        elif s[1] == "июн":
            s[1] = 6
        elif s[1] == "июл":
            s[1] = 7
        elif s[1] == "авг":
            s[1] = 8
        elif s[1] == "сен":
            s[1] = 9
        elif s[1] == "окт":
            s[1] = 10
        elif s[1] == "ноя":
            s[1] = 11
        elif s[1] == "дек":
            s[1] = 12
        if len(s) == 2:
            s.append(2023)
        else:
            s[2] = int(s[2])
        return date(s[2], s[1], s[0])


def logIn(browser):
    browser.get("https://ok.ru/dk?st.cmd=anonymMain&st.layer.cmd=PopLayerClose")
    browser.find_element(By.NAME, "st.email").send_keys(...) # email
    browser.find_element(By.NAME, "st.password").send_keys(...) # password
    browser.find_element(By.NAME, "st.password").send_keys(Keys.ENTER)


def getPostText(page_post):
    text_post = ""
    text_blocks = page_post.find("div", class_="media-layer_c").find_all("div", class_="media-text_cnt_tx")
    for block in text_blocks:
        text_post = text_post + block.text.strip() + "\n"
    return text_post


def writePostPhotos(conn, cur, photos, cnt_media, id_media, id_post):
    for item in photos:
        try:
            file_link = item.find("a").get("href")
            db.insertMedia(conn, cur, id_media, id_post, "post", "https://ok.ru" + file_link, "image")
            id_media += 1
        except:
            cnt_media -= 1
    return cnt_media, id_media


def writePostVideos(conn, cur, videos, cnt_media, id_media, id_post):
    for item in videos:
        try:
            file_link = item.find("a").get("href")
            db.insertMedia(conn, cur, id_media, id_post, "post", "https://ok.ru" + file_link, "video")
            id_media += 1
        except:
            cnt_media -= 1
    return cnt_media, id_media


def writePostAudios(conn, cur, audios, cnt_media, id_media, id_post):
    for item in audios:
        try:
            file_link = item.find("a", class_="track-with-cover_name").get("href")
            db.insertMedia(conn, cur, id_media, id_post, "post", "https://ok.ru" + file_link, "audio")
            id_media += 1
        except:
            cnt_media -= 1
    return cnt_media, id_media


def getPostMedia(page_post):
    photos = page_post.find("div", class_="mlr_cnt").find_all("div", class_="media-photos_photo")
    videos = page_post.find("div", class_="mlr_cnt").find_all("div", class_="media-video")
    audios = page_post.find("div", class_="mlr_cnt").find_all("div", class_="track-with-cover")
    cnt_media = len(photos) + len(videos) + len(audios)
    return photos, videos, audios, cnt_media


def writePostMedia(conn, cur, photos, videos, audios, cnt_media, id_media, id_post):
    cnt_media, id_media = writePostPhotos(conn, cur, photos, cnt_media, id_media, id_post)
    cnt_media, id_media = writePostVideos(conn, cur, videos, cnt_media, id_media, id_post)
    cnt_media, id_media = writePostAudios(conn, cur, audios, cnt_media, id_media, id_post)
    return cnt_media, id_media


def getComments(page_post):
    comments = page_post.find("div", class_="comments_lst").find_all("div", class_="comments_current")
    cnt_comments = len(comments)
    return comments, cnt_comments


def getLikes(page_post):
    try:
        cnt_likes = int(page_post.find("div", class_="mlr_bot").find("span", class_="feed_info_sm_a").text.split()[0])
    except:
        cnt_likes = 0
    return cnt_likes


def writePost(conn, cur, id_post, link_post, date_post, text_post, cnt_comments, cnt_media, cnt_likes, id_group):
    db.insertPost(conn, cur, id_post, link_post, date_post, text_post, cnt_comments, cnt_media, cnt_likes, id_group)
    db.updateGroup(conn, cur, id_group, cnt_likes)


def updateCommentUser(conn, cur, user_name, item, id_user):
    if db.findUserByName(cur, user_name) == 0:
        link_user = item.find("a", class_="comments_author-name").get("href")
        db.insertUser(conn, cur, id_user, "https://ok.ru" + link_user, user_name, 1)
        id_user += 1
    else:
        db.updateUser(conn, cur, db.findUserByName(cur, user_name))
    return id_user


def writeCommentVideos(conn, cur, comment_videos, cnt_comment_media, id_media, id_comment):
    for item in comment_videos:
        try:
            file_link = item.find("a").get("href")
            db.insertMedia(conn, cur, id_media, id_comment, "comment", "https://ok.ru" + file_link, "video")
            id_media += 1
        except:
            cnt_comment_media -= 1
    return cnt_comment_media, id_media


def writeCommentPhotos(conn, cur, comment_photos, cnt_comment_media, id_media, id_comment):
    for item in comment_photos:
        try:
            file_link = item.find("a").get("href")
            db.insertMedia(conn, cur, id_media, id_comment, "comment", "https://ok.ru" + file_link, "image")
            id_media += 1
        except:
            cnt_comment_media -= 1
    return cnt_comment_media, id_media


def writeCommentAudios(conn, cur, comment_audios, cnt_comment_media, id_media, id_comment):
    for item in comment_audios:
        try:
            file_link = item.find("a", class_="track-with-cover_name").get("href")
            db.insertMedia(conn, cur, id_media, id_comment, "comment", "https://ok.ru" + file_link, "audio")
            id_media += 1
        except:
            cnt_comment_media -= 1
    return cnt_comment_media, id_media


def getCommentMedia(comment):
    comment_audios = comment.find_all("div", class_="track-with-cover")
    comment_photos = comment.find_all("div", class_="collage_i")
    comment_videos = comment.find_all("div", class_="media-video")
    cnt_comment_media = len(comment_videos) + len(comment_audios) + len(comment_photos)
    return comment_audios, comment_photos, comment_videos, cnt_comment_media


def writeCommentMedia(conn, cur, comment_videos, comment_photos, comment_audios, cnt_comment_media, id_media, id_comment):
    cnt_comment_media, id_media = writeCommentVideos(conn, cur, comment_videos, cnt_comment_media, id_media, id_comment)
    cnt_comment_media, id_media = writeCommentPhotos(conn, cur, comment_photos, cnt_comment_media, id_media, id_comment)
    cnt_comment_media, id_media = writeCommentAudios(conn, cur, comment_audios, cnt_comment_media, id_media, id_comment)
    return cnt_comment_media, id_media


def parsComments(conn, cur, comments, id_user, id_comment, id_media, id_post):
    for comment in comments:
        user_name = comment.find("a", class_="comments_author-name").find("span").text.strip()
        id_user = updateCommentUser(conn, cur, user_name, comment, id_user)
        comment_text = comment.find("span", class_="js-text-full").text.strip()
        comment_user_id = db.findUserByName(cur, user_name)
        comment_date = dateFormat(comment.find("span", class_="comments_current__footer__main__date").text.strip())
        comment_audios, comment_photos, comment_videos, cnt_comment_media = getCommentMedia(comment)
        cnt_comment_media, id_media = writeCommentMedia(conn, cur, comment_videos, comment_photos, comment_audios, cnt_comment_media, id_media, id_comment)
        db.insertComment(conn, cur, id_comment, comment_date, id_post, comment_user_id, comment_text, cnt_comment_media)
        id_comment += 1
    return id_user, id_comment, id_media


def parsPost(conn, cur, browser, id_group, id_post, id_media, id_comment, id_user):
    page_post = BeautifulSoup(browser.page_source, 'lxml')
    link_post = browser.current_url
    date_post = dateFormat(page_post.find("div", class_="group-author-bottom__kzqdm").find("time").text.strip())
    text_post = getPostText(page_post)
    photos, videos, audios, cnt_media = getPostMedia(page_post)
    cnt_media, id_media = writePostMedia(conn, cur, photos, videos, audios, cnt_media, id_media, id_post)
    comments, cnt_comments = getComments(page_post)
    cnt_likes = getLikes(page_post)
    writePost(conn, cur, id_post, link_post, date_post, text_post, cnt_comments, cnt_media, cnt_likes, id_group)
    id_user, id_comment, id_media = parsComments(conn, cur, comments, id_user, id_comment, id_media, id_post)
    return id_media, id_comment, id_user, link_post


def waitNextPost(browser, link_post):
    waiting = 0
    while browser.current_url == link_post:
        time.sleep(0.1)
        waiting += 0.1
        if waiting == 25:
            print("Группа не собрана до конца((")
            print("Время ожидания превышено. Либо попалась баганая кнопка, либо очень плохое интернет-соединение.\n")
            return False
    return True


def getNextPost(browser):
    try:
        browser.find_element(By.CLASS_NAME, "arw__next").click()
        return True
    except:
        print("Ура! Группа успешно собрана!!!\n")
        return False


def parsGroup(conn, cur, browser, group, id_post, id_media, id_comment, id_user):
    db.insertGroup(conn, cur, group[0], group[1], group[2], 0, 0)
    browser.get(group[3])
    while True:
        id_media, id_comment, id_user, link_post = parsPost(conn, cur, browser, group[0], id_post, id_media, id_comment, id_user)
        id_post += 1
        if not getNextPost(browser):
            return id_post, id_media, id_comment, id_user
        if not waitNextPost(browser, link_post):
            return id_post, id_media, id_comment, id_user
