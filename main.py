from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util import getMsgList, getImgList, writeMsgList, writeImgList
import time
import os

print('---QQ空间小爬虫---')
print('-使用说明：')
print('-1、请确保您已登录QQ（下面脚本会打开浏览器，您可在浏览器中扫码登录）')
print('-2、该爬虫只允许爬取QQ好友')
print('-3、请确保您已安装 Chrome 以及对应版本的 chromedriver，并在下面指定 chromedriver.exe 路径')

pageIndex = 1
imgNumber = 1
qqNumber = input('输入爬取的好友QQ号：').strip()
foldPath = './result/' + qqNumber
imgPath = foldPath + '/images'
textPath = foldPath + '/text'

# 请把下面路径改为你本地 chromedriver.exe 的实际路径
CHROMEDRIVER_PATH = r"\chromedriver.exe"

service = Service(executable_path=CHROMEDRIVER_PATH)
browser = webdriver.Chrome(service=service)
wait = WebDriverWait(browser, 15)

browser.get('https://user.qzone.qq.com/' + qqNumber + '/311')

# 创建存档目录
os.makedirs(imgPath, exist_ok=True)
os.makedirs(textPath, exist_ok=True)
print('图像库和文档库创建完成..')

# 因为 QQ 登录通常需要扫码或滑块，建议手动登录一次
input('浏览器已打开，请在浏览器中完成登录（扫码或输入密码等）。完成后在此处按回车继续...')

try:
    while True:
        browser.save_screenshot('temp.png')

        # 输出抓取页码
        print('正在抓取..第' + str(pageIndex) + '页说说')
        pageIndex += 1

        # 进入空间主内容所在的 frame（等待出现）
        frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.app_canvas_frame')))
        browser.switch_to.frame(frame)

        # 获取说说列表--文字部分
        time.sleep(1.0)
        contexts = browser.find_elements(By.CLASS_NAME, 'content')
        dates = browser.find_elements(By.CSS_SELECTOR, '.c_tx.c_tx3.goDetail')
        msgList = getMsgList(contexts, dates)
        writeMsgList(msgList, textPath)

        # 获取说说列表--图片部分
        time.sleep(1.0)
        # 注意：title 属性里可能是中文“查看大图”，采用精确匹配
        imageAnchors = browser.find_elements(By.CSS_SELECTOR, '[title="查看大图"]')
        imgList = getImgList(imageAnchors)
        imgNumber = writeImgList(imgList, imgNumber, imgPath)

        time.sleep(1.0)
        # 切换回默认内容再点击下一页按钮（下一页按钮一般在默认上下文里）
        browser.switch_to.default_content()
        try:
            next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="下一页"]')))
            next_btn.click()
            # 等待页面跳转并短暂停顿
            time.sleep(2.0)
        except Exception:
            print('未找到下一页，爬取结束')
            break

except Exception as e:
    print('发生异常，停止爬取：', e)
finally:
    browser.quit()
    print('浏览器已关闭')