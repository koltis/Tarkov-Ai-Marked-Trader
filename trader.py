import sys
from PIL import Image
from pytesseract import pytesseract
import os
import random
import threading
import time
import cv2
import numpy as np
import pyautogui
import numpy
from PIL import Image
from productList import getNextProduct
path_to_tesseract = r"C:\Users\kolti\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract


Rublo = cv2.imread(r'imgs\rublos.png')
Rublo = cv2.cvtColor(Rublo, cv2.COLOR_BGR2GRAY)
revenue = 0
failedAttends = 0


def calcRevenue(maxPrice, price):
    global revenue
    revenue = revenue + (maxPrice - price)


def matchTwoImages(imageTemplate, searchedImg, threshold, extraWidht=20, extraHeight=20,  pixelCorrection={'x': 0, 'y': 0}, showMatches=False):
    print("start match")
    imageTemplate = cv2.cvtColor(
        imageTemplate, cv2.COLOR_BGR2GRAY)

    matchTwoImagesResult = cv2.matchTemplate(
        imageTemplate, searchedImg, cv2.TM_CCOEFF_NORMED)

    w = searchedImg.shape[1]
    h = searchedImg.shape[0]
    loc = np.where(matchTwoImagesResult >= threshold)

    response = []

    for (x, y) in zip(*loc[::-1]):
        x = x - pixelCorrection.get('x')
        y = y - pixelCorrection.get('y')

        regionOfInteres = imageTemplate[y: y +
                                        h + extraHeight, x: x + w + extraWidht]

        cv2.rectangle(imageTemplate, (x, y), (x + w + extraWidht,
                                              y + h + extraHeight), (0, 0, 255), 2)

        response.append(
            {"x": x, "y": y, "regionOfInteres": regionOfInteres})

    # this code shows what the ai Image capture tecnology captures
    if showMatches:
        cv2.imshow('Tarkov Game Screen', imageTemplate)
        cv2.waitKey(0)
    print("finish match")
    return response


def imageToText(image, text=False, number=False, mix=True):

    text = pytesseract.image_to_string(
        image, lang='eng', config='tessedit_char_whitelist=0123456789')

    textWithoutCharacters = ""

    for x in text:

        try:
            if number:
                int(x)
                textWithoutCharacters += str(x)
            else:
                textWithoutCharacters += x
        except:
            None
    return textWithoutCharacters


def getProductPrices(imageTemplate, searchedImg, threshold, extraWidht, extraHeight):

    pixelCorrection = {'x': 124, 'y': 9}

    matchingResults = matchTwoImages(
        imageTemplate, searchedImg, threshold, extraWidht, extraHeight, pixelCorrection)

    prices = []
    print("productPrices")
    print(len(matchingResults))
    # iteration tester
    # iteration = 0
    for result in matchingResults:
        # this code prints image regionOfInterest on imageToText soo u can see what is going wrong
        # cv2.imwrite(r'imgs\imageToText.png', result.get("regionOfInteres"))

        if prices:
            if prices[-1].get("y") >= result.get("y") - 10 and prices[-1].get("y") >= result.get("y") - 10:
                if not prices[-1].get("price"):
                    price = imageToText(image=result.get(
                        "regionOfInteres"), number=True)
                    result["price"] = price
                    prices.append(result)
                elif result.get("price") != prices[-1].get("price"):
                    pass
            else:
                price = imageToText(image=result.get(
                    "regionOfInteres"), number=True)
                result["price"] = price
                prices.append(result)
        else:
            price = imageToText(image=result.get(
                "regionOfInteres"), number=True)
            result["price"] = price
            prices.append(result)
        # iteration test
        # iteration += 1
        # print(iteration)

    return prices


def checkSuccess(recursion=None):
    # take a screenshoot of a succes and fail buy proccess an upload the pìctures to https://pixspy.com/ to get the cords of a succes al failing pixel to check for color
    # this process should be made by ai but im to lazy ;:D:D:D:D:D:D:D::D and since is a message with opacity im to lazy to think about all variables i let that
    # job to whoever wants it
    time.sleep(0.5)
    checkSuccessScreenShoot = pyautogui.screenshot()
    # checkSuccessScreenShoot = Image.open(r'imgs\checkSuccessScreenShoot.png')
    print("save")
    # checkSuccessScreenShoot.save(r'imgs\checkSuccessScreenShoot.png')
    pix = checkSuccessScreenShoot.load()

    success = {"y": 1368, "x":  1911, "RGB>": {"r": 200, "g": 200, "b": 200}}
    fail = {"y": 1376, "x": 1913, "RGB>": {
        "r": 200, "g": (30, 90), "b": (30, 90)}}

    succesRGB = pix[success.get("x"), success.get("y")]
    failRGB = pix[fail.get("x"), fail.get("y")]
    print(succesRGB, failRGB)
    print(pix[success.get("x"), success.get("y")])

    print(pix[fail.get("x"), fail.get("y")])
    if succesRGB[0] > success.get("RGB>").get("r") and succesRGB[1] > success.get("RGB>").get("g") and succesRGB[2] > success.get("RGB>").get("b"):
        return True
    elif failRGB[0] > fail.get("RGB>").get("r") and (failRGB[1] > fail.get("RGB>").get("g")[0] and failRGB[1] < fail.get("RGB>").get("g")[1]) and (
        failRGB[2] > fail.get("RGB>").get(
            "b")[0] and failRGB[2] < fail.get("RGB>").get("b")[1]
    ):
        return False
    else:
        if not recursion:
            return checkSuccess(1)
        else:
            solveCaptcha()
            return False


def buyProduct(name, maxPrice, ):
    im1 = pyautogui.screenshot()
    im1.save(r'imgs\image1.png')
    Tarkov_Screen_Image = cv2.imread(r'imgs\image1.png')
    productsPrices = getProductPrices(imageTemplate=Tarkov_Screen_Image,
                                      searchedImg=Rublo, threshold=0.64, extraWidht=95, extraHeight=10,)
    # boughtOne = False
    # i will keep this as a foor couse i need to think about the best way of doing it regarts the page reloading and
    # img analisis what is better? i will leave a for soo is easy to change it with out problems as needed
    if not productsPrices:
        nextProduct = getNextProduct(name)
        print("Switching to : ",
              nextProduct['name'], ", max price : ", nextProduct['price'])
        searchProduct(nextProduct['name'])
        buyProduct(nextProduct['name'], nextProduct['price'])
    else:
        for price in productsPrices:
            print("precio:", price.get("price"))

            try:
                if int(float(price.get("price"))) < maxPrice:

                    print("comprar precio:", price.get("price"))
                    print("y:", price.get("y"), ",", "x:", price.get("x"))
                    pyautogui.click(price.get("x")+600, price.get("y")+20)
                    time.sleep(0.3)
                    # I need to check if i want to click in all and buy all or not couse the risk of an error i cant read.
                    pyautogui.keyDown("y")
                    pyautogui.keyUp("y")
                    boughtOne = checkSuccess()
                    time.sleep(0.4)
                    global failedAttends
                    # this time is to check where is clicliking since if u have diferent resolution than me it wont work
                    # time.sleep(5)
                    if boughtOne:
                        print("Bought: ", boughtOne)
                        calcRevenue(maxPrice=int(maxPrice),
                                    price=int(float(price.get("price"))))
                        print("Total revenue: ", revenue)
                        failedAttends = 0
                    else:
                        print("Bought: ", boughtOne)

                        checkSuccessScreenShoot = pyautogui.screenshot()
                        pix = checkSuccessScreenShoot.load()

                        outOfStockHeader = pix[1227, 656]
                        outOfStockBody = pix[1447, 733]

                        if ((outOfStockBody[0] == 0 and outOfStockBody[1] == 0 and outOfStockBody[2] == 0)
                                and (outOfStockHeader[0] == 25 and outOfStockHeader[1] == 27 and outOfStockHeader[2] == 27)):
                            pyautogui.sleep(0.2)
                            pyautogui.click(1288, 753)
                            sellAll()
                            pyautogui.click(1652, 1418)
                            pyautogui.sleep(0.2)
                            print("All sold")
                            nextProduct = getNextProduct(name)
                            print("Switching to : ",
                                  nextProduct['name'], ", max price : ", nextProduct['price'])
                            searchProduct(nextProduct['name'])
                            buyProduct(nextProduct['name'],
                                       nextProduct['price'])

                    reloadPage()
                    buyProduct(name, maxPrice)
                    break
                else:
                    # call function to get new product with price
                    print("To expensive :" + name)
                    nextProduct = getNextProduct(name)
                    print("Switching to : ",
                          nextProduct['name'], ", max price : ", nextProduct['price'])
                    searchProduct(nextProduct['name'])
                    buyProduct(nextProduct['name'], nextProduct['price'])

            except ValueError:
                nextProduct = getNextProduct(name)
                print("Switching to : ",
                      nextProduct['name'], ", max price : ", nextProduct['price'])
                searchProduct(nextProduct['name'])
                buyProduct(nextProduct['name'], nextProduct['price'])


def reloadPage():
    # reload button cords
    pyautogui.click(2453, 160)
    time.sleep(0.6)


def searchProduct(name):
    # search on product dictionary to get price

    # use https://pixspy.com/ to get pixel of the search input mine is (x:258 , y:151)
    pyautogui.click(258, 151)
    pyautogui.write(name, interval=0.05)
    pyautogui.keyDown('enter')
    time.sleep(0.2)
    pyautogui.keyUp('enter')
    time.sleep(0.8)

    # use https://pixspy.com/ to get pixel of the first product select mine is (x:234 , y:215)
    pyautogui.doubleClick(234, 215)
    time.sleep(0.5)
    # click on page reload just in case
    reloadPage()


def getNextColor(imgPix, expectedPixel, relativePixel=0, xCord=0, xCordLimit=0, xCordDefault=0,  yCord=0, yCordLimit=0, yCordDefault=0, up=False, prevPixelColor={"RGB>": {"r": 4, "g": 21, "b": 42}}, checkPrev=False):
    # this function get cords of the pixel where color changes for captcha and maybe other uses in the future

    prevPixel = {"r": 1, "g": 1, "b": 1}

    foundColor = False
    limit = False

    fromCord = xCord if not xCordDefault else yCord
    toCord = xCordLimit if not xCordDefault else yCordLimit

    while ((fromCord > toCord and (not limit)) if not up else (fromCord < toCord and (not limit))):
        captchaRGB = imgPix[
            fromCord, yCordDefault] if not xCordDefault else imgPix[
            xCordDefault, fromCord]
        if relativePixel:
            if (captchaRGB[0] + relativePixel.get("RGB>").get("r") >= expectedPixel.get("RGB>").get("r") and captchaRGB[0] - relativePixel.get("RGB>").get("r") <= expectedPixel.get("RGB>").get("r")) and \
                (captchaRGB[1] + relativePixel.get("RGB>").get("g") >= expectedPixel.get("RGB>").get("g") and captchaRGB[1] - relativePixel.get("RGB>").get("g") <= expectedPixel.get("RGB>").get("g")) and \
                    (captchaRGB[2] + relativePixel.get("RGB>").get("b") >= expectedPixel.get("RGB>").get("b") and captchaRGB[2] - relativePixel.get("RGB>").get("b") <= expectedPixel.get("RGB>").get("b")):
                foundColor = True
                limit = True
            else:
                prevPixel.update({
                    "r": captchaRGB[0],
                    "g": captchaRGB[1],
                    "b": captchaRGB[2]
                })
                fromCord = fromCord - 1 if not up else fromCord + 1
        else:
            if captchaRGB[0] == expectedPixel.get("RGB>").get("r") and captchaRGB[1] == expectedPixel.get("RGB>").get("g") and captchaRGB[2] == expectedPixel.get("RGB>").get("b"):
                if checkPrev:
                    if prevPixel["r"] == prevPixelColor["RGB>"]["r"] and prevPixel["g"] == prevPixelColor["RGB>"]["g"] and prevPixel["b"] == prevPixelColor["RGB>"]["b"]:
                        foundColor = True
                        limit = True
                else:
                    foundColor = True
                    limit = True
            else:
                prevPixel.update({
                    "r": captchaRGB[0],
                    "g": captchaRGB[1],
                    "b": captchaRGB[2]
                })
                fromCord = fromCord - 1 if not up else fromCord + 1
    return fromCord


def getBlueCords(captchaPix,  expectedCaptchaPixel, halfScreen):
    # get more or less the half of your screen

    minY = 200

    maxBlueY = getNextColor(imgPix=captchaPix, expectedPixel=expectedCaptchaPixel,
                            xCordDefault=halfScreen["x"], yCord=halfScreen["y"], yCordLimit=minY)
    if maxBlueY:

        lowestblueY = getNextColor(imgPix=captchaPix, expectedPixel={"RGB>": {"r": 0, "g": 0, "b": 0}},
                                   xCordDefault=halfScreen["x"], yCord=maxBlueY, yCordLimit=minY)
        # -1 since its outside the blue we found the black
        lowestblueY = lowestblueY - 1

        minBlueX = getNextColor(imgPix=captchaPix, expectedPixel={"RGB>": {"r": 0, "g": 0, "b": 0}},
                                yCordDefault=maxBlueY, xCord=halfScreen["x"], xCordLimit=450)

        maxBlueX = getNextColor(imgPix=captchaPix, expectedPixel={"RGB>": {"r": 0, "g": 0, "b": 0}},
                                yCordDefault=maxBlueY, xCord=halfScreen["x"], xCordLimit=2060, up=True)

        # to get your 58 get the px distnace bettwen the maxBlueY and the end of the static 2 paragraph message on the top of the captcha using https://pixspy.com/

        return {"toY": maxBlueY, "fromY":    lowestblueY + 58, "fromX": minBlueX, "toX": maxBlueX - 1}
    else:
        return False


def getCaptchaCords(captchaPix,  expectedCaptchaPixel, halfScreen):

    maxXCaptcha = getNextColor(imgPix=captchaPix, expectedPixel=expectedCaptchaPixel,
                               yCordDefault=halfScreen["y"], xCord=halfScreen["x"], xCordLimit=2060, up=True, prevPixelColor={"RGB>": {"r": 22, "g": 24, "b": 25}})

    minXCaptcha = getNextColor(imgPix=captchaPix, expectedPixel=expectedCaptchaPixel,
                               yCordDefault=halfScreen["y"], xCord=halfScreen["x"], xCordLimit=420, prevPixelColor={"RGB>": {"r": 88, "g": 93, "b": 96}})

    maxYCaptcha = getNextColor(imgPix=captchaPix, expectedPixel=expectedCaptchaPixel,
                               xCordDefault=halfScreen["x"], yCord=halfScreen["y"], yCordLimit=1500, up=True, prevPixelColor={"RGB>": {"r": 8, "g": 8, "b": 8}})

    minYCaptcha = getNextColor(imgPix=captchaPix, expectedPixel=expectedCaptchaPixel,
                               xCordDefault=halfScreen["x"], yCord=halfScreen["y"], yCordLimit=206,  prevPixelColor={"RGB>": {"r": 14, "g": 15, "b": 15}})

    return {"toY": maxYCaptcha, "fromY": minYCaptcha, "fromX": minXCaptcha, "toX": maxXCaptcha}


def clearResults(matchingResults, promptedObjectImg):
    matches = []
    for result in matchingResults:
        if matches:
            # here i would need to do loop over the matches to clear the results not only over the last match
            found = False
            for match in matches:
                if (match.get("y") >= result.get("y") - (promptedObjectImg.shape[0]/1.7) and match.get("y") <= result.get("y") + (promptedObjectImg.shape[0]/1.7)
                    ) and (
                        match.get("x") >= result.get("x") -
                    (promptedObjectImg.shape[1]/1.7) and match.get(
                        "x") <= result.get("x") + (promptedObjectImg.shape[1]/1.7)
                ):
                    found = True
            if not found:
                print()
                result["y"] = int(
                    result["y"] + promptedObjectImg.shape[0]/3)
                result["x"] = int(
                    result["x"] + promptedObjectImg.shape[1]/3)
                matches.append(result)
        else:

            result["y"] = int(result["y"] + promptedObjectImg.shape[0]/3)
            result["x"] = int(result["x"] + promptedObjectImg.shape[1]/3)
            matches.append(result)

    return matches


def solveCaptcha(depth=0):
    # for testing purposes
    # captchaImg = Image.open(r'imgs\captcha.png')

    captchaImg = pyautogui.screenshot()
    captchaImg.save(r'imgs\captcha.png')
    captchaPix = captchaImg.load()
    halfScreen = {"x": 1248, "y": 734}
    expectedCaptchaPixel = {"y": 404, "x": 1028, "RGB>": {
        "r": 4, "g": 21, "b": 42}}

    cords = getBlueCords(captchaPix=captchaPix,
                         expectedCaptchaPixel=expectedCaptchaPixel, halfScreen=halfScreen)

    if cords:
        # check for default values is those are the cords means there is no captcha :D
        if cords["toY"] != 200 and cords["fromY"] != 257 and cords["fromX"] != 450 and cords["toX"] != 2059:
            cropedCaptcha = captchaImg.crop(
                (cords["fromX"], cords["fromY"], cords["toX"], cords["toY"]))

            promptedObject = imageToText(cropedCaptcha)
            promptedObject = promptedObject.strip()
            print("the captcha is asking for :", promptedObject)

            cords = getCaptchaCords(captchaPix=captchaPix, expectedCaptchaPixel={
                                    "RGB>": {"r": 0, "g": 0, "b": 0}}, halfScreen=halfScreen)

            cropedCaptcha = captchaImg.crop(
                (cords["fromX"], cords["fromY"], cords["toX"], cords["toY"]))

            open_cv_image = numpy.array(cropedCaptcha.convert('RGB'))
            open_cv_image = open_cv_image[:, :, ::-1].copy()

            objUrl = r'captchaImgs\ '.strip()
            objUrl = objUrl + promptedObject + '.png'
            promptedObjectImg = cv2.imread(
                objUrl)

            promptedObjectImg = cv2.cvtColor(
                promptedObjectImg, cv2.COLOR_BGR2GRAY)

            # to show the croped captcha and the promptedObject
            # cv2.imshow('prompted object', promptedObjectImg)
            # cv2.waitKey(0)
            # cv2.imshow('cropedimg template', open_cv_image)
            # cv2.waitKey(0)

            matchingResults = matchTwoImages(
                imageTemplate=open_cv_image, searchedImg=promptedObjectImg, showMatches=True, threshold=0.65)

            # print(matchingResults)
            matches = clearResults(
                matchingResults=matchingResults, promptedObjectImg=promptedObjectImg)

            """
            for result in matchingResults:
                if matches:
                    if (matches[-1].get("y") >= result.get("y") - (promptedObjectImg.shape[0]/2) and matches[-1].get("y") >= result.get("y") - (promptedObjectImg.shape[0]/2)
                        ) and (
                            matches[-1].get("x") >= result.get("x") -
                        (promptedObjectImg.shape[1]/2) and matches[-1].get(
                            "x") >= result.get("x") - (promptedObjectImg.shape[1]/2)
                    ):
                        pass
                    else:

                        matches.append(result)
                else:

                    matches.append(result)
            """

            print(len(matches))
            print(matches)
            if matches:
                for match in matches:
                    print({"x": match["x"] + int(promptedObjectImg.shape[1]/4) + cords["fromX"],
                           "y": match["y"] + int(promptedObjectImg.shape[0]/4) + cords["fromY"]})

                    pyautogui.click(match["x"] + cords["fromX"],
                                    match["y"] + cords["fromY"])
                    time.sleep(0.1)

                time.sleep(0.3)

                # average distance bettwen the topY and the middle of the confirm button https://pixspy.com/

                pyautogui.click(halfScreen["x"], cords["toY"] + 51)
            else:
                if depth <= 4:
                    depth = depth + 1
                    solveCaptcha(depth=depth)
                else:
                    raise ValueError(
                        "something went wrong on the captcha fixer")
        else:
            pass
    else:
        pass
    # get top y and the topY + default message size and i get the y from where i can crop the image to get the item name.


def scroll(scrollbar):
    inventoryImg = pyautogui.screenshot()
    inventoryPix = inventoryImg.load()
    cords = getNextColor(imgPix=inventoryPix, expectedPixel={"RGB>": {
        "r": 175, "g": 185, "b": 191}}, relativePixel={"RGB>": {"r": 30, "g": 30, "b": 30}},
        xCordDefault=scrollbar["x"], yCord=scrollbar["y"], yCordLimit=1338, up=True)
    """
    cords = getNextColor(imgPix=inventoryPix, expectedPixel={"RGB>": {
        "r": 175, "g": 185, "b": 191}},
        xCordDefault=scrollbar["x"], yCord=scrollbar["y"], yCordLimit=1338, up=True)
    """

    print("cords", cords)

    if cords < scrollbar['maxY']:
        print("click locuelo :D")
        print(scrollbar['x'], cords + int(scrollbar["ySize"]/3))
        print(cords, scrollbar['ySize'])

        pyautogui.click(scrollbar['x'], cords + scrollbar["ySize"]/3)

        scroll = 2
        while (scroll):
            pyautogui.sleep(0.1)
            pyautogui.keyDown("down")
            pyautogui.keyUp("down")
            print(scroll, "scroll")
            scroll = scroll - 1


def sellAndScroll(productName):
    scrollbar = {"xSize": 11, "ySize": 187, "x": 2540, "y": 352, "maxY": 1336}
    scrolls = 5
    while (scrolls):
        sellProduct(productName=productName)
        pyautogui.sleep(0.2)
        sellProduct(productName=productName+"Rt")
        scroll(scrollbar)
        scrolls = scrolls - 1
        print(scrolls, "scrolls")

    pyautogui.click(scrollbar['x'], scrollbar["y"], 10)
    while (scrolls <= 10):
        pyautogui.keyDown("up")
        pyautogui.keyUp("up")
        scrolls = scrolls + 1


def sellProduct(productName):

    inventoryImg = pyautogui.screenshot()

    cropedInventoryImg = inventoryImg.crop(
        (1250, 0, 2557, 1437))

    open_cv_image = numpy.array(cropedInventoryImg.convert('RGB'))
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    objUrl = r'imgs\ '.strip()
    objUrl = objUrl + productName + '.png'
    promptedObjectImg = cv2.imread(
        objUrl)
    promptedObjectImg = cv2.cvtColor(
        promptedObjectImg, cv2.COLOR_BGR2GRAY)

    matchingResults = matchTwoImages(
        imageTemplate=open_cv_image, searchedImg=promptedObjectImg, threshold=0.65, extraWidht=0, extraHeight=0)
    print("matches")
    matches = clearResults(matchingResults=matchingResults,
                           promptedObjectImg=promptedObjectImg)
    # this solves a bug with the ui
    pyautogui.click(1291, 382)
    for match in matches:
        print(match)
        pyautogui.keyDown("ctrl")
        pyautogui.sleep(0.2)
        pyautogui.doubleClick(match["x"]+1250, match["y"])
        pyautogui.sleep(0.01)
        pyautogui.keyUp("ctrl")
        pyautogui.sleep(0.05)
        pyautogui.click(1291, 382)
        pyautogui.sleep(0.2)


def sellAll():
    pyautogui.click(1470, 1425)
    time.sleep(0.2)

    traders = {"therapist": {
        "x": 259, "y": 167, "products": ["Pressure gauge", 'Battered antique book',  "Fuel conditioner", "roler submariner", "Can of condensed milk", "Flat Screwdriver (long)", "Bottle of OLOLO Multivitamins", "pipe grip wrench", "Axel parrot", "gingy keychain", "Analog thermometer"]

    }, "ragman": {
        "x": 1098, "y": 170, "products": ["Glorious E lightweight"]
    }}
    for trader in traders:
        print(traders[trader])
        pyautogui.click(traders[trader]["x"], traders[trader]["y"])
        time.sleep(1)

        for product in traders[trader]["products"]:
            print(product)
            time.sleep(2)
            sellAndScroll(productName=product)


# solveCaptcha(0)
# sellAll()
# sellAndScroll("pipe grip wrench")

nextProduct = getNextProduct()
searchProduct(name=nextProduct['name'])
buyProduct(name=nextProduct['name'], maxPrice=nextProduct['price'])

# solveCaptcha()
# im1 = pyautogui.screenshot()
# im1.save(r'imgs\seller.png')
# scroll()
# check blue box captcha pixel check cords {'x':1029,'y':347, 'RGB>':{"r": 4, "g": 21, "b": 42}}
# blue box text cords from {'x':1035,'y':404} to {'x': 1528 , 'y':433}
