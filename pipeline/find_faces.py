# Given a list of directories/filenames, find faces, output JSON.
import argparse
import os

import cv2
import json

def setup(haar_cascade_directory=None):
    haar_cascade_directory = haar_cascade_directory or "/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades"
    face_cascade = cv2.CascadeClassifier(os.path.join(haar_cascade_directory, 'haarcascade_frontalface_default.xml'))
    return face_cascade

def find_face(photo_metadata, cv_img, face_cascade):
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces

def crop_face(photo_metadata, cv_img, face_xywh):
    x, y, w, h = face_xywh
    crop_img = cv_img[y: y+h, x: x+w]
    return crop_img

def get_face_path(photo_metadata):
    return os.path.basename(photo_metadata['filename'])
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find some faces.')
    parser.add_argument("--haar_cascade_directory", default=None)
    parser.add_argument("--input_image")
    parser.add_argument("--output_directory", default="output")
    args = parser.parse_args()

    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)
    
    face_cascade = setup()
    cv_img = cv2.imread(args.input_image)
    img_metadata = {
        'filename': args.input_image
    }
    output_metadata = {
        'img_metadata': img_metadata,
        'faces': []
    }
    face_data = find_face(img_metadata, cv_img, face_cascade)
    face_directory = os.path.join(args.output_directory, get_face_path(img_metadata))
    if not os.path.exists(face_directory):
        os.makedirs(face_directory)

    for i, face in enumerate(face_data):
        output_metadata['faces'].append(face.tolist())
        crop_img = crop_face(img_metadata, cv_img, face)
        cv2.imwrite(os.path.join(face_directory, "face%d.jpg" % i), crop_img)
    with open(os.path.join(face_directory, "face.json"), 'w') as f:
        print >>f, json.dumps(output_metadata)
        
    #cv2.rectangle(cv_img,(x,y),(x+w,y+h),(255,0,0),2)
    #roi_gray = gray[y:y+h, x:x+w]
    #roi_color = cv_img[y:y+h, x:x+w]
