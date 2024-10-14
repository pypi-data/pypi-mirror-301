from imports import *
from feat import Detector
from feat.utils.io import read_feat

def silent_tqdm(*args, **kwargs):
    return tqdm(*args, **kwargs, disable=True)

import feat.detector
feat.detector.tqdm = silent_tqdm

class PyFeat_Detection:
    def calculate_bounding_box(self, temp_path, number_faces, confidence=.9):
        '''
        Input needed: temp_frame_path, num_faces
        
        '''
        detector = Detector(
            face_model='retinaface',
            landmark_model='mobilefacenet',
            au_model='xgb',
            emotion_model='resmasknet',
            facepose_model='img2pose',
            device='cpu',
            face_threshold=confidence
        )
        bounding_boxes = [] # box around rectangle stored as (x, y, w, h)
        detections = detector.detect_image(temp_path, )

        filtered_detections = []
        for index, row in detections.iterrows():
            if not pd.isna(row['FaceRectX']) and not pd.isna(row['FaceRectY']) and not pd.isna(row['FaceRectWidth']) and not pd.isna(row['FaceRectHeight']):
                x, y, w, h = int(row['FaceRectX']), int(row['FaceRectY']), int(row['FaceRectWidth']), int(row['FaceRectHeight'])
                if w > 50 and h > 50: # only adds 'faces' larger than 50 x 5, needs to be determined manually
                    filtered_detections.append(row)

        # only saves num_faces number of faces, ordered based on FaceScore (confidence)
        filtered_detections = sorted(filtered_detections, key=lambda x: x['FaceScore'], reverse=True)[:number_faces]

        for r in filtered_detections:
            bounding_boxes.append((int(r['FaceRectX']), int(r['FaceRectY']), int(r['FaceRectWidth']), int(r['FaceRectHeight'])))
        
        return filtered_detections, bounding_boxes