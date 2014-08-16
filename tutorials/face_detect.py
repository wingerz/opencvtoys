import sys

import numpy as np
import cv2


def scale_dimensions(x, y, long_side=900):
    x_is_long = False
    if x > y:
        x_is_long = True
    if x_is_long:
        new_dimensions = (long_side, int(round(float(y)* long_side/x)))
    else:
        new_dimensions = (int(round(float(x)*long_side/y)), long_side)
    return new_dimensions

def resize(img, long_side=600):
    old_dimensions = img.shape
    new_dimensions = scale_dimensions(old_dimensions[0], old_dimensions[1], long_side=long_side)
    return cv2.resize(img, tuple(reversed(new_dimensions)))

if __name__ == "__main__":
    filename = sys.argv[1]
    face_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_eye.xml')

    img = cv2.imread(filename)
    img = resize(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print "found %d faces" % len(faces)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
