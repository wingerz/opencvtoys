import os
import sys

import cv2
import json

if __name__ == "__main__":
    image_directory = sys.argv[1]
    with open(os.path.join(image_directory, 'face.json')) as f:
        metadata_str = f.readline()
    metadata = json.loads(metadata_str)
    img = cv2.imread(metadata['img_metadata']['filename'])
    for x, y, w, h in metadata['faces']:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
    cv2.imshow('faces',img)
    cv2.waitKey(0)
