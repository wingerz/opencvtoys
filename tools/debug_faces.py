import os
import sys

import cv2
import json


def scale_dimensions(x, y, long_side=900):
    x_is_long = False
    if x > y:
        x_is_long = True
    if x_is_long:
        ratio = float(long_side) / x
        new_dimensions = (long_side, int(round(float(y)* long_side/x)))
    else:
        ratio = float(long_side) / y
        new_dimensions = (int(round(float(x)*long_side/y)), long_side)
    return new_dimensions, ratio

def resize(img, long_side=1200):
    old_dimensions = img.shape
    new_dimensions, ratio = scale_dimensions(old_dimensions[0], old_dimensions[1], long_side=long_side)
    return cv2.resize(img, tuple(reversed(new_dimensions))), ratio

def px_scale(length, ratio):
    return int(round(length * ratio))


if __name__ == "__main__":
    image_directory = sys.argv[1]
    with open(os.path.join(image_directory, 'face.json')) as f:
        metadata_str = f.readline()
    metadata = json.loads(metadata_str)
    img = cv2.imread(metadata['img_metadata']['filename'])
    resized_img, ratio = resize(img)
    
    for x, y, w, h in metadata['faces']:
        x, y, w, h = [px_scale(l, ratio) for l in [x, y, w, h]]
        cv2.rectangle(resized_img, (x, y), (x+w, y+h),(255,0,0),2)
    
    cv2.imshow('faces',resized_img)
    cv2.waitKey(0)
