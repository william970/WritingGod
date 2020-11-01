import cv2
import numpy as np
from math import *

def rotate_lh(img,degree):
    height_ori,width_ori=img.shape[:2]
    height_1=int(width_ori*fabs(sin(radians(degree)))+height_ori*fabs(cos(radians(degree))))
    width_1=int(height_ori*fabs(sin(radians(degree)))+width_ori*fabs(cos(radians(degree))))
    matRotation=cv2.getRotationMatrix2D((width_ori/2,height_ori/2),degree,1)
    matRotation[0,2] +=(width_1-width_ori)/2
    matRotation[1,2] +=(height_1-height_ori)/2
    imgRotation=cv2.warpAffine(img,matRotation,(width_1,height_1),borderValue=(255,255,255))
    return imgRotation

def docRot(src_img_c):
    src_img = cv2.cvtColor(src_img_c,cv2.COLOR_RGB2GRAY)
    if(src_img is None):
        return 0
    opWidth = cv2.getOptimalDFTSize(src_img.shape[0]);
    opHeight = cv2.getOptimalDFTSize(src_img.shape[1]);
    padded=cv2.copyMakeBorder(src_img,0,opWidth-src_img.shape[0], 0, opHeight-src_img.shape[1], cv2.BORDER_CONSTANT, value=(0,0,0))
    a=padded.astype(np.float64)
    b=np.zeros(a.shape,float)
    comImg=cv2.merge([a,b])
    comImg=cv2.dft(comImg)
    c=cv2.split(comImg)[0]
    d=cv2.split(comImg)[1]
    e=cv2.magnitude(c,d)
    f=e+1
    g=np.log10(f)
    height=g.shape[0]
    width=g.shape[1]
    if(g.shape[0]%2==1):
        height=g.shape[0]-1
    if(g.shape[1]%2==1):
        width=g.shape[1]-1
    g=g[0:width,0:height]
    cx=int(g.shape[1]/2)
    cy=int(g.shape[0]/2)
    q0=g[0:cx,0:cy];
    q1=g[0:cx,cy:2*cy];
    q2=g[cx:2*cx,cy:2*cy];
    q3=g[cx:2*cx,0:cy];
    temp=q0
    q0=q2
    q2=temp
    temp=q1
    q1=q3
    q3=temp
    cv2.normalize(g, g, 0, 1, cv2.NORM_MINMAX);
    h=g*255
    _,k=cv2.threshold(h,150,255,cv2.THRESH_BINARY);
    l=k.astype(np.uint8)
    lines = cv2.HoughLines(l,1,np.pi/180,100,0,0)
    if(lines is None):
        return 0
    angel=0
    # count = 0
    for line in lines:
        theta=line[0,1]
        if(abs(theta)<np.pi/45 or abs(theta-np.pi/2)<np.pi/45):
        # if(theta<30*np.pi/180 or np.pi-theta<30*np.pi/180):
            continue
        else:
            angel=theta
            break
    #         angel = angel + theta
    #         count = count + 1
    # angel = angel/count
    angel=angel if angel<np.pi/2 else angel-np.pi
    if(angel != np.pi/2):
        angelT = src_img.shape[0]*np.tan(angel)/src_img.shape[1]
        angel = np.arctan(angelT)
    angelD = angel*180/float(np.pi)
    if 45 - angelD < 0:
        angelD = angelD - 90
    elif angelD < -45:
        angelD = angelD + 90
    # imgRotation=rotate_lh(src_img,angelD)
    imgRotation_c=rotate_lh(src_img_c,angelD)
    # return angelD
    # cv2.imshow("src_img_c",src_img_c)
    return imgRotation_c

if __name__ == '__main__':
    img = cv2.imread("../../data/demo/auto_save_2018-01-26 125826.jpg")
    img = docRot(img)
    cv2.imshow("imgRotation",img)
    cv2.waitKey(0)