import sys
from PIL import Image
from pytesseract import pytesseract
import os
import random
import threading
import time
import cv2
import numpy as np
from mss import mss
# import keyboard
# import multiprocessing

path_to_tesseract = r"C:\Users\kolti\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
image_path = r"/imgs/imageToText.png"


def image_to_text(image_path):

    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(
        image_path, lang='eng', config='tessedit_char_whitelist=0123456789')

    text_without_characters = ""
    for x in text:
        try:
            int(x)
            text_without_characters += str(x)
        except:
            None


def match_two_images(game_image, image_looking, threshold_value, extra_widht, extra_height, text):
    match_two_images_result = cv2.matchTemplate(
        game_image, image_looking, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_two_images_result)

    w = image_looking.shape[1]
    h = image_looking.shape[0]

    threshold = threshold_value
    yloc, xloc = np.where(match_two_images_result >= threshold)
    for (x, y) in zip(xloc, yloc):
        print(y, x, w, h)
        x = x - 60
        if text == "Rublo":
            region_of_interest = Tarkov_Screen_Image[y:y +
                                                     h + extra_height - 10, x:x + w + extra_widht - 30]
            print(region_of_interest)
            image_to_text(region_of_interest)

        cv2.rectangle(Tarkov_Screen_Image, (x, y), (x + w + extra_widht, y + h + extra_height),
                      (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)

        cv2.putText(Tarkov_Screen_Image, text, (x - 55, y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


if __name__ == '__main__':
    Tarkov_Screen_Image = cv2.imread(r'imgs\image1.png')
    Tarkov_Screen_Image = cv2.cvtColor(Tarkov_Screen_Image, cv2.COLOR_BGR2GRAY)

    Rublo = cv2.imread(r'imgs\rublos.png')
    Rublo = cv2.cvtColor(Rublo, cv2.COLOR_BGR2GRAY)

    # cv2.putText(Tarkov_Screen_Image, "Made by Ains", (147, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 1)

    match_two_images(game_image=Tarkov_Screen_Image, image_looking=Rublo,
                     threshold_value=0.67, extra_widht=75, extra_height=10, text="Rublo")

    # dino_game_images = cv2.resize(dino_game_images, (0, 0), fx=0.4, fy=0.4)

    cv2.imshow('Tarkov Game Screen', Tarkov_Screen_Image)
    cv2.waitKey(0)
