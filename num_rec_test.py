import cv2

img=cv2.imread('assets/sun_test.png',0)
ret,thresh=cv2.threshold(img,127,255,0)
edges=cv2.Canny(img,100,200)