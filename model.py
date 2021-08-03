# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
import easyocr


def Car_Name_Plate(img):
    # Reading the Image
    img = cv2.imread(img)
    # Gray Image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # plt.imshow(gray,cmap="gray")
    b_filter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise Reduction
    edged = cv2.Canny(b_filter, 30, 200)  # Edge Detection
    # plt.imshow(edged,cmap="gray")
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    # plt.imshow(new_image)
    (x, y) = np.where(mask == 255)
    (X1, y1) = (np.min(x), np.min(y))
    (X2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[X1:X2 + 1, y1:y2 + 1]
    # plt.imshow(cropped_image,cmap='gray')
    reader = easyocr.Reader(['en'])
    results = reader.readtext(cropped_image)
    text = results[0][-2]
    font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1] + 60), fontFace=font, fontScale=1,
                      color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0, 255, 0), 3)
    plt.imshow(res)
    plt.show()