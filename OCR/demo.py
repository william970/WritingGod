# -*- coding:utf-8 -*-
import ocr
import cv2
import pyautogui
import time
import numpy as np
from PIL import Image
from glob import glob
import re
import matplotlib.pyplot as plt
import random
import json

image_files = glob('C:\\Users\\10\\Documents\\雷电模拟器\\Pictures\\Screenshots\\*.png')
Name = 1


def randomchar():
    return chr(random.randint(97, 122))


def randomName():
    global Name
    Name += 1
    return str(Name)


def reread():
    pyautogui.click(1842, 89)
    pyautogui.click(1752, 432)


def showall():
    pyautogui.moveTo(1329, 298)
    pyautogui.mouseDown()
    time.sleep(1)
    pyautogui.mouseUp()


def cv_imread(filePath):
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    ## imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
    ##cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
    return cv_img


def write_json(obj):
    '''
    写入/追加json文件
    :param obj:
    :return:
    '''

    # 首先读取已有的json文件中的内容
    item_list = {}
    with open('data.json', 'r', encoding='utf-8') as f:
        load_dict = json.load(f)
        train_item = load_dict['train']
    # 读取已有内容完毕
    # 将新传入的dict对象追加至list中
    for i in range(len(obj)):
        train_item.append(obj[i])
    item_list['train'] = train_item
    # 将追加的内容与原有内容写回（覆盖）原文件
    with open('data.json', 'w', encoding='utf-8') as f2:
        json.dump(item_list, f2, ensure_ascii=False)


# obj字典对象为新增内容
# obj = {"id": 10,"text": "DATE","background_color": "#7c20e0","text_color": "#ffffff"}
# write_json(obj)


if __name__ == '__main__':
    filename = "data.json"
    lastrose = 600
    nameMap = {}
    nameMap["白夜"] = "Name1"
    finish = False
    while not finish:
        # pyautogui.click(1329, 298)
        pyautogui.scroll(1000)
        reread()
        showall()
        pyautogui.scroll(-140)
        time.sleep(1)
        im = pyautogui.screenshot(region=(1323, 40, 1876 - 1323, 1024 - 40))
        im = np.array(im)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        blurImg = cv2.medianBlur(gray, 5)
        circles = cv2.HoughCircles(blurImg, cv2.HOUGH_GRADIENT,
                                   1, 120, param1=100, param2=30,
                                   minRadius=20, maxRadius=40)
        rose = []
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                rose.append(i[1])
        else:
            circles = []

        # for i in circles[0, :]:
        #     rose.append(i[1])
        #     cv2.circle(im, (i[0], i[1]), i[2], (0, 255, 0), 4)
        # plt.figure(figsize=(20, 20))
        # plt.imshow(im)
        # plt.show()
        # 如果找到的头像数量小于2的话
        if len(rose) < 2:
            print(rose)
            rose = [984]
            sortrose = [984]
            # print(sortrose)
            print("找到的头像坐标小于2取固定的坐标：" + str(1024 - 40))
            indexH = 1024 - 40
            pyautogui.moveTo(1329, indexH)
            pyautogui.dragTo(1200, 28 + 45, 2, button='left')
            time.sleep(0.1)
            im2 = pyautogui.screenshot(region=(1323, 40, 1876 - 1323, 1024 - 40))
            im2 = np.array(im2)
            time.sleep(1)
            # plt.figure(figsize=(20, 20))
            # plt.imshow(im2)
            # plt.show()
            difference = cv2.subtract(im, im2)
            result = not np.any(difference)
        else:
            sortrose = sorted(rose)
            lastrose = sortrose[-1]
            print(rose)
            print(sortrose)
            print("找到最后一个头像坐标:" + str(lastrose))
            indexH = 40 + lastrose
            pyautogui.moveTo(1329, indexH)
            pyautogui.dragTo(1200, 28 + 45, 2, button='left')
            time.sleep(0.1)
            im2 = pyautogui.screenshot(region=(1323, 40, 1876 - 1323, 1024 - 40))

            im2 = np.array(im2)
            time.sleep(1)
            # plt.figure(figsize=(20, 20))
            # plt.imshow(im2)
            # plt.show()
            difference = cv2.subtract(im, im2)
            result = not np.any(difference)
        while (not result):
            x, y = im.shape[0:2]
            im = im[0:lastrose - 22, ]
            # plt.figure(figsize=(20, 20))
            # plt.imshow(im)
            # plt.show()
            print(im.shape)
            im = cv2.resize(im, (int(im.shape[1] * 2), int(im.shape[0] * 2)))
            for j in range(len(sortrose)):
                sortrose[j] = sortrose[j] * 2
            cv2.bitwise_not(im, im)
            shape = im.shape
            print(shape)
            result, image_framed, isname = ocr.model(im, sortrose, nameMap)
            print("\nRecognition Result:\n")
            total = []
            str1 = ""
            flag = False
            for key in result:
                out = result[key][1]
                # print(str(isname[key]) + ":" + out)
                if isname[key] == 1:
                    if str1 != "":
                        if str1.find(":") != -1:
                            if str1.split(":")[-1] != "":
                                total.append(str1)
                                str1 = ""
                        else:
                            if str1 != "":
                                str1 = "scene:" + str1
                                total.append(str1)
                                str1 = ""

                    if out not in nameMap:
                        if 5 > len(out) > 1:
                            nameMap[out] = "Name" + randomName()
                            str1 = nameMap[out] + ":"
                    else:
                        str1 = nameMap[out] + ":"
                elif isname[key] == 2:
                    if str1.find(":") != -1:
                        if str1.split(":")[-1] != "":
                            total.append(str1)
                            str1 = ""
                    else:
                        if str1 != "":
                            str1 = "scene:" + str1
                            total.append(str1)
                            str1 = ""
                else:
                    str1 += out
                if out.find("完结啦") != -1 or out.find("全文完") != -1:
                    finish = True
                    break
                if (out.find("此话已啃光啦") != -1
                        or out.find("和作者互动") != -1
                        or out.find("本章完") != -1
                        or out.find("此活已啃光") != -1):
                    flag = True
                    break
            if isname[key] == 0:
                if str1.find(":") != -1:
                    if str1.split(":")[-1] != "":
                        total.append(str1)
                        str1 = ""
                else:
                    if str1 != "":
                        str1 = "scene:" + str1
                        total.append(str1)
                        str1 = ""
            write_json(total)
            if finish:
                break
            if flag:
                break
            im = im2
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            blurImg = cv2.medianBlur(gray, 5)
            circles = cv2.HoughCircles(blurImg, cv2.HOUGH_GRADIENT,
                                       1, 120, param1=100, param2=30,
                                       minRadius=20, maxRadius=40)
            rose = []
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    rose.append(i[1])
            else:
                circles = []

            # 如果找到的头像数量小于2的话
            if len(rose) < 2:
                print(rose)
                # print(sortrose)
                print("找到的头像坐标小于2取固定的坐标：" + str(1024 - 40))
                indexH = 1024 - 40
                pyautogui.moveTo(1329, indexH)
                pyautogui.dragTo(1200, 28 + 45, 2, button='left')
                time.sleep(0.1)
                im2 = pyautogui.screenshot(region=(1323, 40, 1876 - 1323, 1024 - 40))
                im2 = np.array(im2)
                time.sleep(1)
                # plt.figure(figsize=(20, 20))
                # plt.imshow(im2)
                # plt.show()
                difference = cv2.subtract(im, im2)
                result = not np.any(difference)
                continue
            sortrose = sorted(rose)
            lastrose = sortrose[-1]
            print(rose)
            print(sortrose)
            print("找到最后一个头像坐标:" + str(lastrose))
            indexH = 40 + lastrose
            pyautogui.moveTo(1329, indexH)
            pyautogui.dragTo(1200, 28 + 45, 2, button='left')
            time.sleep(0.1)
            im2 = pyautogui.screenshot(region=(1323, 40, 1876 - 1323, 1024 - 40))
            im2 = np.array(im2)
            time.sleep(1)
            # plt.figure(figsize=(20, 20))
            # plt.imshow(im2)
            # plt.show()
            difference = cv2.subtract(im, im2)
            result = not np.any(difference)
        # 确保到底
        pyautogui.click(1329, 298)
        for i in range(20):
            print(i)
            pyautogui.scroll(-1000)
        time.sleep(1)
        pyautogui.click(1670, 969)
