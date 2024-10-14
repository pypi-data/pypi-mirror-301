from imports import *
import mediapipe as mp

class MediaPipe_Detection:
    def calculate_bounding_box(self, temp_path, number_faces, confidence=0.7):
        '''
        Input needed: temp_frame_path, num_faces
        
        '''
        mp_face_detection = mp.solutions.face_detection

        bounding_boxes = []
        filtered_detections = []
        image = cv2.imread(temp_path)
        height, width, _ = image.shape

        with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=confidence) as face_detection:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image_rgb)

            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    x, y, w, h = int(bboxC.xmin * width), int(bboxC.ymin * height), int(bboxC.width * width), int(bboxC.height * height)

                    if w > 50 and h > 50:
                        filtered_detections.append({
                            'FaceRectX': x, 
                            'FaceRectY': y, 
                            'FaceRectWidth': w, 
                            'FaceRectHeight': h, 
                            'FaceScore': detection.score[0]  
                        })

        filtered_detections = sorted(filtered_detections, key=lambda x: x['FaceScore'], reverse=True)[:number_faces]

        for r in filtered_detections:
            bounding_boxes.append((r['FaceRectX'], r['FaceRectY'], r['FaceRectWidth'], r['FaceRectHeight']))
        filtered_detections_df = pd.DataFrame(filtered_detections)
        
        return filtered_detections_df, bounding_boxes