import argparse
import json
import os
import pprint




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Find some faces.')
    parser.add_argument("--face_img_directory", default="output")
    parser.add_argument("--out", default="all_faces.json")
    args = parser.parse_args()

    faces_data = []
    stats = {}
    for root, dirs, files in os.walk(args.face_img_directory):
        if 'face.json' in files:
            with open(os.path.join(root, 'face.json')) as f:
                line = f.readline()
                face_data = json.loads(line)
                faces_data.append(face_data)
                
    stats['count_image_total'] = len(faces_data)
    
    faces_data = [face_data for face_data in faces_data if face_data['faces']]
    stats['count_image_with_faces'] = len(faces_data)
    stats['count_faces'] = sum([len(face_data['faces']) for face_data in faces_data])

    with open(args.out, 'w') as f:
        for face_data in faces_data:
            print >>f, json.dumps(face_data)
    
    
