import cv2
from numpy import uint8, frombuffer, shape, average, array
from pytesseract import  pytesseract, image_to_string
from configparser import ConfigParser

configur = ConfigParser()
configur.read('config.ini')

pytesseract.tesseract_cmd = configur.get('tesseract', 'path')

def read_img(image, resize=1, thresh_min=240):

    nparr = frombuffer(image, uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    avg = int(find_avg_color(gray))

    if avg > 127:
        thresh_method = cv2.THRESH_BINARY
        thresh_min = avg - 50
    else:
        thresh_method = cv2.THRESH_BINARY_INV
        if avg <= 30:
            thresh_min = 140 + avg
        else:
            thresh_min = 10 + avg

    h, w = gray.shape

    # resizing image so tesseract would be able to read it
    if resize == 1 and (h < 1000 or w < 1000):
        resize = 1000 / (h if (h < w) else w)

    gray = cv2.resize(gray, (0, 0), fx=resize, fy=resize)

    ret, thresh = cv2.threshold(gray, thresh_min, 255, thresh_method)

    im2 = thresh.copy()

    text = image_to_string(im2)

    return text


def find_avg_color(image):
    height, width = shape(image)

    # calculate the average color of each row of our image
    avg_color_per_row = average(image, axis=0)

    # calculate the averages of our rows
    avg_colors = average(avg_color_per_row, axis=0)

    # so, convert that array to integers
    int_average = array(avg_colors, dtype=uint8)

    return int_average
