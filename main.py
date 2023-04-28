from selenium import webdriver
import time
import os

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By

cookies = [
    {'domain': '.ximalaya.com', 'httpOnly': False, 'name': '1_l_flag', 'path': '/', 'sameSite': 'Lax', 'secure': False,
     'value': '54798548&C5F49150340NCC1A063BA399EE316B5B14E9ABAC72EFC660A578CBA7A4891B004443B5F8C6D8111MBB3797E9455A57F__2023-03-2115:32:04'},
    {'domain': '.ximalaya.com', 'expiry': 1713943924, 'httpOnly': True, 'name': '1&_token', 'path': '/',
     'sameSite': 'Lax', 'secure': False,
     'value': '54798548&C5F49150340NCC1A063BA399EE316B5B14E9ABAC72EFC660A578CBA7A4891B004443B5F8C6D8111MBB3797E9455A57F_'},
    {'domain': 'www.ximalaya.com', 'httpOnly': False, 'name': 'web_login', 'path': '/', 'sameSite': 'Lax',
     'secure': False, 'value': '1679383942715'},
    {'domain': '.ximalaya.com', 'expiry': 1713943924, 'httpOnly': False, 'name': '1&remember_me', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': 'y'},
    {'domain': '.ximalaya.com', 'expiry': 1710919924, 'httpOnly': False,
     'name': 'Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070', 'path': '/', 'sameSite': 'Lax', 'secure': False,
     'value': '1679383915'},
    {'domain': '.ximalaya.com', 'httpOnly': False, 'name': 'impl', 'path': '/', 'sameSite': 'Lax', 'secure': False,
     'value': 'www.ximalaya.com.login'},
    {'domain': '.ximalaya.com', 'httpOnly': False, 'name': 'Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': '1679383925'},
    {'domain': '.ximalaya.com', 'httpOnly': False, 'name': 'xm-page-viewid', 'path': '/', 'sameSite': 'Lax',
     'secure': False, 'value': 'ximalaya-web'},
    {'domain': '.ximalaya.com', 'httpOnly': False, 'name': 'x_xmly_traffic', 'path': '/', 'sameSite': 'Lax',
     'secure': False,
     'value': 'utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A'},
    {'domain': '.ximalaya.com', 'expiry': 1713943911, 'httpOnly': False, 'name': '_xmLog', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': 'h5&1213a3f8-8640-40f8-bb8f-8218c40bbd71&process.env.sdkVersion'}
]

album_url = "https://www.ximalaya.com/album/70349771"
album_tracks = []
if __name__ == '__main__':

    driver = webdriver.Chrome()

    # 导入cookie免登陆
    driver.get('http://www.ximalaya.com')
    for cookie in cookies:
        driver.add_cookie(cookie)

    # 进入专辑页面
    driver.get(album_url)
    time.sleep(5)

    # 获得专辑信息： 先要上下滑动一下窗口， 才能让浏览器生成完整的内容。之后才能获取到
    # 先点击一下展开更多按钮
    bnt_more = driver.find_element(By.CLASS_NAME, 'more-intro-wrapper')
    input_comment = driver.find_element(By.ID, 'anchor_sound_list')

    ActionChains(driver) \
        .scroll_to_element(input_comment) \
        .perform()
    time.sleep(2)
    bnt_more.click()
    time.sleep(2)
    ActionChains(driver) \
        .scroll_to_element(input_comment) \
        .perform()
    ActionBuilder(driver).clear_actions()

    album_description = driver.find_element(By.TAG_NAME, "article").text
    album_title = driver.find_element(By.CLASS_NAME, "info").find_element(By.CLASS_NAME, "title").text
    print(f'album title: {album_title}')
    print(f"introduction: \n{album_description}")
    with open("./audio/0-" + album_title + ".txt", mode="w", encoding='utf-8') as f:
        f.write(album_description)
    # 获取列表页数
    page_items = driver.find_element(By.CLASS_NAME, "pagination") \
        .find_elements(By.CLASS_NAME, "page-item")
    no_of_pages = int(page_items[-2].text)
    print(f"the number of the pages is {no_of_pages}")
    # 下载所有有声书url
    # 获取列表跳转输入元素
    input_text = driver.find_element(By.CSS_SELECTOR, "form>input[type='number']")
    # print(input_text.get_attribute("placeholder"))

    # 获得跳转按钮的输入元素
    input_btn = driver.find_element(By.CSS_SELECTOR, "form>button[type='submit']")
    # print(input_btn.text)

    # 跳转每个页面，获得列表
    for page_id in (no_of_pages - i for i in range(no_of_pages)):
        print(f"jump to page {page_id}")
        # 跳转
        input_text.send_keys(str(page_id))
        input_btn.click()
        time.sleep(3)

        # 获得所有页面
        track_list = driver.find_element(By.CSS_SELECTOR, ".sound-list"). \
            find_element(By.TAG_NAME, "ul"). \
            find_elements(By.TAG_NAME, "li")
        print(f'Len of track list: {len(track_list)}')

        # 取出每个条目的信息
        for li in track_list:
            t_id = li.find_element(By.CLASS_NAME, 'num').text
            t_title = li.find_element(By.CLASS_NAME, 'title').text
            t_link = li.find_element(By.TAG_NAME, 'a').get_attribute("href")
            t_item = (t_id, t_title, t_link)
            album_tracks.append(t_item)
            print(t_item)

    # 遍历每个track，获取信息
    for item in album_tracks:
        driver.get(item[2])
        time.sleep(10)

        # 先点击一下展开更多按钮

        try:
            bnt_more = driver.find_element(By.CLASS_NAME, 'more-intro-wrapper')
            input_comment = driver.find_element(By.CLASS_NAME, 'comment-input-area')
            input_comment.send_keys("hi,ximalaya")
            ActionChains(driver) \
                .scroll_to_element(input_comment) \
                .perform()
            time.sleep(5)
            bnt_more.click()
            ActionChains(driver) \
                .scroll_to_element(input_comment) \
                .pause(1) \
                .perform()
            ActionBuilder(driver).clear_actions()
            # 获取完整文字内容

        except NoSuchElementException:
            pass
        finally:
            pass

        try:
            t_intro = driver.find_element(By.TAG_NAME, 'article').text
        except NoSuchElementException:
            t_intro = None
        finally:
            pass

        # print(f"{item[0]} {item[1]} \nintroduction: \n{t_intro}")
        # 点击播放按钮 并获得语音文件的url
        bnt_play = driver.find_element(By.CLASS_NAME, "play-btn")
        ActionChains(driver) \
            .scroll_to_element(bnt_play) \
            .pause(1) \
            .perform()
        ActionBuilder(driver).clear_actions()
        bnt_play.click()
        time.sleep(5)
        audio_url = driver.execute_script("return $webPlayer.currentTrack.src")
        t_item = item + (t_intro, audio_url)
        print(t_item)
        if t_intro:
            with open("./audio/" + item[0] + "-" + item[1].replace(" ", "\ ") + ".txt", mode="w",
                      encoding='utf-8') as f:
                f.write(t_intro)
        str_curl = "curl '" + audio_url + "' --compressed --output " + "./audio/" + item[0] + "-" + item[1].replace(" ", "\ ") + ".mp3"
        print("call #" + str_curl)
        os.system(str_curl)

    # 结束
    driver.quit()

    # input_text.send_keys(page_items[1])

    # time.sleep(30)
    # # audio = driver.find_element(By.TAG_NAME, "audio")
    #
    # audio = driver.execute_script("return $webPlayer.currentTrack.src")
    # print(audio)

    # print(driver.get_cookies())
