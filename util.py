import re
import requests
from selenium.webdriver.common.by import By

def getMsgList(contexts, dates):
    msgList = list()
    tagPattern = re.compile('<img.*?>|<a.*?>|</a>')
    for i in range(0, len(contexts)):
        raw_msg = contexts[i].get_attribute('innerHTML')
        raw_date = dates[i].get_attribute('innerHTML')

        # 除去内嵌标签
        tags = tagPattern.findall(raw_msg)
        for tag in tags:
            raw_msg = raw_msg.replace(tag, '')

        msgList.append((raw_msg, raw_date))
    return msgList


def writeMsgList(msgList, textPath):
    for msg in msgList:
        with open(textPath + '/qzone.txt', 'a', encoding='utf-8') as f:
            f.write(msg[1])
            f.write('\n')
            f.write(msg[0])
            f.write('\n\n')


def getImgList(imageAnchors):
    imgList = list()
    for anchor in imageAnchors:
        # 使用新版定位（调用者传入的是 anchor 元素）
        imageTag = anchor.find_element(By.CSS_SELECTOR, 'img')
        # 有些页面把真实地址放在 data-src，有些直接在 src
        src = imageTag.get_attribute('data-src') or imageTag.get_attribute('src')
        if src:
            imgList.append(src)
    return imgList


def writeImgList(imgList, imgNumber, imgPath):
    for imgSrc in imgList:
        print('正在下载..' + imgSrc)
        try:
            data = requests.get(imgSrc, timeout=15).content
            with open(imgPath + '/' + str(imgNumber) + '.jpg', 'wb') as f:
                f.write(data)
            imgNumber += 1
        except Exception as e:
            print('下载失败:', imgSrc, e)
    return imgNumber