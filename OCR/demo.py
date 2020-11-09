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

image_files = glob('C:\\Users\\10\\Documents\\雷电模拟器\\Pictures\\Screenshots\\*.png')

def randomchar():
    return chr(random.randint(97, 122))

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


if __name__ == '__main__':
    nameMap = {}
    while True:
        # pyautogui.click(1329, 298)
        pyautogui.scroll(280)
        reread()
        showall()
        pyautogui.scroll(-140)
        time.sleep(5)
        im = pyautogui.screenshot(region=(1323, 40, 1876 - 1323, 1024 - 40))
        im = np.array(im)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        blurImg = cv2.medianBlur(gray, 5)
        circles = cv2.HoughCircles(blurImg, cv2.HOUGH_GRADIENT,
                                   1, 120, param1=100, param2=30,
                                   minRadius=20, maxRadius=40)
        circles = np.uint16(np.around(circles))

        rose = []
        for i in circles[0, :]:
            rose.append(i[1])
            cv2.circle(im, (i[0], i[1]), i[2], (0, 255, 0), 4)
        # plt.figure(figsize=(20, 20))
        # plt.imshow(im)
        # plt.show()
        sortrose = sorted(rose)
        lastrose = sortrose[-1]
        print(rose)
        print(sortrose)
        print("找到最后一个头像坐标:" + str(lastrose))
        indexH = 40 + lastrose
        pyautogui.moveTo(1329, indexH)
        pyautogui.dragTo(1200, 28 + 60, 2, button='left')
        time.sleep(0.1)
        im2 = pyautogui.screenshot(region=(1323, 40, 1876 - 1323, 1024 - 40))

        im2 = np.array(im2)
        time.sleep(5)
        # plt.figure(figsize=(20, 20))
        # plt.imshow(im2)
        # plt.show()
        difference = cv2.subtract(im, im2)
        result = not np.any(difference)
        while (not result):
            x, y = im.shape[0:2]
            im = im[0:lastrose - 22, ]
            plt.figure(figsize=(20, 20))
            plt.imshow(im)
            plt.show()
            print(im.shape)
            im = cv2.resize(im, (int(im.shape[1] * 2), int(im.shape[0] * 2)))
            for j in range(len(sortrose)):
                sortrose[j] = sortrose[j] * 2
            cv2.bitwise_not(im, im)
            shape = im.shape
            print(shape)
            result, image_framed, isname = ocr.model(im, sortrose)
            print("\nRecognition Result:\n")
            total = ""
            flag = False
            for key in result:
                out = result[key][1]
                # print(str(isname[key]) + ":" + out)
                if isname[key] == 1:
                    if out not in nameMap:
                        nameMap[out] = " Name" + randomchar() + randomchar()
                        total = total + nameMap[out] + ":"
                    else:
                        total = total + nameMap[out] + ":"
                else:
                    total = total + out
                if (out.find("此话已啃光啦") != -1
                        or out.find("和作者互动") != -1
                        or out.find("本章完") != -1
                        or out.find("此活已啃光") != -1):
                    flag = True
                    break
            print(total)
            if flag:
                break
            im = im2
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            blurImg = cv2.medianBlur(gray, 5)
            circles = cv2.HoughCircles(blurImg, cv2.HOUGH_GRADIENT,
                                       1, 120, param1=100, param2=30,
                                       minRadius=20, maxRadius=40)
            circles = np.uint16(np.around(circles))

            rose = []
            for i in circles[0, :]:
                rose.append(i[1])
            # 如果找到的头像数量小于2的话
            if len(rose) < 2:
                print(rose)
                print(sortrose)
                print("找到的头像坐标小于2取固定的坐标：" + str(1024 - 40))
                indexH = 1024 - 40
                pyautogui.moveTo(1329, indexH)
                pyautogui.dragTo(1200, 28 + 60, 2, button='left')
                time.sleep(0.1)
                im2 = pyautogui.screenshot(region=(1323, 40, 1876 - 1323, 1024 - 40))
                im2 = np.array(im2)
                time.sleep(5)
                # plt.figure(figsize=(20, 20))
                # plt.imshow(im2)
                # plt.show()
                difference = cv2.subtract(im, im2)
                result = not np.any(difference)
            sortrose = sorted(rose)
            lastrose = sortrose[-1]
            print(rose)
            print(sortrose)
            print("找到最后一个头像坐标:" + str(lastrose))
            indexH = 40 + lastrose
            pyautogui.moveTo(1329, indexH)
            pyautogui.dragTo(1200, 28 + 60, 2, button='left')
            time.sleep(0.1)
            im2 = pyautogui.screenshot(region=(1323, 40, 1876 - 1323, 1024 - 40))
            im2 = np.array(im2)
            time.sleep(5)
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
