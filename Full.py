import pyautogui, time
import pytesseract.pytesseract
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import date
import pytesseract
from PIL import Image
import re
import pandas as pd
import json
import datetime
import pickle
# Mở tab
def tools_all():
    driver = webdriver.Chrome(r"C:\Users\DELL\Downloads\chromedriver_win32\chromedriver.exe")
    driver.get("https://www.topcv.vn/viec-lam")
    time.sleep(5)

    pyautogui.click(50, 50)
    fw = pyautogui.getActiveWindow()
    fw.maximize()
    time.sleep(3)

    #  Auto tìm việc data engineer và press enter
    x, y = (0.08 * fw.width), (0.32 * fw.height)
    pyautogui.click(x, y)
    pyautogui.write('vien thong')  # Tìm việc data engineer
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(2)
    elems = driver.find_elements_by_xpath("//h3[@class='title']//a")
    links = [elem.get_attribute('href') for elem in
                elems]  # Tìm tất cả các link việc làm trong href và mở từng link để screenshot
    x = 0
    title = {}
    congty = {}
    motacongviec = {}
    merge_content_1 = []
    merge_content_2 = []
    title_title = []
    congty_title = []
    content = []
    date=[]
    for i in range(0, 8):
        driver.get(str(links[i]))  # Mở lần lượt các link

        # Title

        try:
            title[i] = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//h1[@class='job-title text-highlight bold']")))
        except:
            title[i] = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//h1[@class='job-name text-premium']")))
        time.sleep(1)
        with open(f"title{str([i, 0])}.png", "wb") as f:
            f.write(title[i][0].screenshot_as_png)

        def process_image(i):
            pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract-ocr\tesseract-ocr\tesseract.exe'
            configuration = ("vie+eng --oem 1 --psm 6")
            try:
                value = pytesseract.image_to_string(Image.open(f"title{str([i, 0])}.png").convert('L'),
                                                        config=configuration, lang='vie')
                text = re.sub("\r|\f", " ", value)
            except ValueError:
                text = " "
            return text

        title_title.append(process_image(i))

        # Congty_title

        try:
            congty[i] = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='company-title']/a")))
        except:
            congty[i] = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@id='company-name']/h1")))
        time.sleep(1)
        with open(f"congty{str([i, 0])}.png", "wb") as f:
            f.write(congty[i][0].screenshot_as_png)

        def process_image(i):
            pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract-ocr\tesseract-ocr\tesseract.exe'
            configuration = ("vie+eng --oem 1 --psm 6")
            try:
                value = pytesseract.image_to_string(Image.open(f"congty{str([i, 0])}.png").convert('L'),
                                                        config=configuration, lang='vie')
                text = re.sub("\r|\f", " ", value)
            except ValueError:
                text = " "
            return text

        congty_title.append(process_image(i))

        # Content

        try:
            motacongviec[i] = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='content-tab']")))
        except:
            motacongviec[i] = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='job-data']/div")))
        time.sleep(1)
        for j in range(0, 3):
            with open(f"motacongviec{str([i, j])}.png", "wb") as f:
                f.write(motacongviec[i][j].screenshot_as_png)  # Chụp ảnh phần công ty yêu cầu công viêc và quyền lợi mức lương

            def process_image(i, j):
                pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract-ocr\tesseract-ocr\tesseract.exe'
                configuration = ("vie+eng --oem 1 --psm 6")
                try:
                    value = pytesseract.image_to_string(Image.open(f"motacongviec{str([i, j])}.png"),
                                                            config=configuration, lang='vie')
                    text = re.sub("\r|\f", " ", value)
                except ValueError:
                    text = " "
                return text

            if j == 0:
                a = 'MÔ TẢ CÔNG VIỆC \n' + process_image(i, j)
                merge_content_1.append(a)
            if j == 1:
                b = 'YÊU CẦU ỨNG VIÊN \n' + process_image(i, j)
                merge_content_1.append(b)
            if j == 2:
                c = 'QUYỀN LỢI ĐƯỢC HƯỞNG \n' + process_image(i, j)
                merge_content_1.append(c)
        content.append(merge_content_1)
        merge_content_1 = []
        date_time = datetime.datetime.now()
        date.append(str(date_time))
    data = {
            'title': title_title,
            'congty': congty_title,
            'content': content,
            'date': date
        }
    df = pd.DataFrame(data=data)
    df.to_csv('df.csv', index=None)
    pickle.dump(df, open('df.pkl', 'wb'))
print(tools_all())