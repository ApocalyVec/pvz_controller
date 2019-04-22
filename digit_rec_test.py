from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import scipy
from PIL import Image
import cv2
import numpy as np
import pytesseract

# DIGITS_LOOKUP = {
#     (1, 1, 1, 0, 1, 1, 1): 0,
#     (0, 0, 1, 0, 0, 1, 0): 1,
#     (1, 0, 1, 1, 1, 1, 0): 2,
#     (1, 0, 1, 1, 0, 1, 1): 3,
#     (0, 1, 1, 1, 0, 1, 0): 4,
#     (1, 1, 0, 1, 0, 1, 1): 5,
#     (1, 1, 0, 1, 1, 1, 1): 6,
#     (1, 0, 1, 0, 0, 1, 0): 7,
#     (1, 1, 1, 1, 1, 1, 1): 8,
#     (1, 1, 1, 1, 0, 1, 1): 9
# }

image=cv2.imread('frames/1.png')
# image = imutils.resize(image, height=500)#\
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image, (5, 5), 0)
image = cv2.Canny(image, 50, 200, 255)

# edge map of the image
# TODO those are hard coded dimensions
image = image[115:150, 30:130]

# cv2.erode(image, np.ones((10,10), np.uint8), iterations=5)

# img = Image.fromarray(image)
# img.show()



"""
Contour extraction
"""
cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None

# loop over the contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # if the contour has four vertices, then we have found
    # the thermostat display
    if len(approx) == 4:
        displayCnt = approx
        break

thresh = cv2.threshold(image, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

img = Image.fromarray(thresh)
img.show()

results = pytesseract.image_to_string(image)
print(results)



# # find contours in the thresholded image, then initialize the
# # digit contours lists
# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#                         cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
# digitCnts = []
#
# # loop over the digit area candidates
# for c in cnts:
#     # compute the bounding box of the contour
#     (x, y, w, h) = cv2.boundingRect(c)
#
#     # if the contour is sufficiently large, it must be a digit
#     if w >= 15 and (h >= 30 and h <= 40):
#         digitCnts.append(c)