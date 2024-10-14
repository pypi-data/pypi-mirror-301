import pandas as pd
import cv2
import csv
import os
import math
import time

class Manual:
    '''
    Each Manual instance is either a dyad (load_specific) or all (load_batch)
    '''
    def __init__(self, path):
        self.input_path = path # Path is the main directory, i.e. /Users/keshavrastogi/Downloads/IPD_Manual
        self.dyad_number = None

    # load in the csv
    def load_batch(self, analyze_type='all', use_existing_one=True):
        print("Loading all available")
        for filename in os.listdir(f"{self.input_path}/videos"):
            output_csv = filename.replace(".mp4", "_ipd.csv").replace("manual_vid_", "")
            if not os.path.exists(f"{self.input_path}/processed/{output_csv}"):
                if analyze_type == "per face":
                    print("Analyzing per face")
                    self.analyze_per_face(f"{self.input_path}/videos/{filename}", use_existing_one)
                else:
                    print("Analzying both faces")
                    self.analyze_all(f"{self.input_path}/videos/{filename}")

    def load_specific(self, dyad_num, analyze_type='all', use_existing_one=True):
        print(f"Loading dyad{dyad_num}")
        self.dyad_number = dyad_num

        for input_csv in os.listdir(f"{self.input_path}/input"):
            if f"_dyad{dyad_num}_" in input_csv and "csv" in input_csv:
                input_c = os.path.join(f"{self.input_path}/input", input_csv)
                output_csv = input_c.replace("input", "processed").replace("manual_csv_", "").replace(f"dyad{dyad_num}", f"dyad{dyad_num}_manual_ipd")

                if not os.path.exists(output_csv):
                    self.load_analyze(input_c, analyze_type, use_existing_one)
                else:
                    override = input(f"Dyad{dyad_num} already processed, Override (y/n): ")
                    if override in ['y', 'yes']:
                        os.remove(output_csv)
                        self.load_analyze(input_c, analyze_type, use_existing_one)


    def load_analyze(self, input, analyze_type, use_existing_one):
        if analyze_type == "per face":
            print("Analzying per face")
            self.analyze_per_face(input, use_existing_one)
        else:
            print("Analyzing both faces")
            self.analyze_all(input)

    def analyze_all(self, input):
        input_csv = input
        input_vid = input_csv.replace(".csv", ".mp4").replace("_csv_", "_vid_")
        print(f"Loading input: {input_vid}")
        output_csv = input.replace("input", "processed").replace("manual_csv_", "").replace(f"dyad{self.dyad_number}", f"dyad{self.dyad_number}_manual_ipd")
        output_vid = output_csv.replace(".csv", "_vid.mp4")

        df = pd.read_csv(input_csv)
        trial_number = df['Trial Number'].iloc[0]

        cap = cv2.VideoCapture(input_vid)
        if not cap.isOpened():
            print("Error: Could not open video.")
            exit()

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_vid, fourcc, 1, (width, height))

        current_index = 0

        while True: # Iterates through each frame in video
            ret, frame = cap.read() 
            if not ret:
                print("End of video")
                break

            points=[]
            status = ["Select first face"]
            first_face_confirmed =[False]
            clicked = [False]
            cv2.namedWindow('Manual Selection')
            cv2.setMouseCallback('Manual Selection', self.mouse_callback_all, (points, status, first_face_confirmed, clicked))

            while True:
                temp_frame = frame.copy()
                if len(points) >= 1:
                    cv2.rectangle(temp_frame, (points[0][0] - 50, points[0][1] - 50), (points[0][0] + 50, points[0][1] + 50), (0, 255, 0), 2)
                if len(points) >= 2:
                    cv2.rectangle(temp_frame, (points[1][0] - 50, points[1][1] - 50), (points[1][0] + 50, points[1][1] + 50), (0, 255, 0), 2)

                self.draw_text_and_rectangle(10, height-15, temp_frame, status[0])
                seconds = df['Second'].iloc[current_index]
                self.draw_text_and_rectangle(width-250, height-15, temp_frame, f"Second: {seconds}")
                self.draw_text_and_rectangle(width // 2 - 150, 30, temp_frame, f"Dyad {self.dyad_number}, Trial {trial_number}")
                cv2.imshow('Manual Selection', temp_frame)

                key = cv2.waitKey(1)
                # if key & 0xFF == 13:  # Enter key
                if key & clicked[0]:
                    if not first_face_confirmed[0] and len(points) == 1:
                        first_face_confirmed[0] = True
                        status[0] = "Select second face"
                    elif first_face_confirmed[0] and len(points) == 2:
                        status[0] = "Confirmed"
                        break
                    clicked[0] = False
                elif key & 0xFF == ord('q'):
                    self.exit(out, cap, output_csv, output_vid, self.dyad_number)
                    return

            bounding_boxes = [(points[0][0] - 50, points[0][1] - 50, 100, 100),
                            (points[1][0] - 50, points[1][1] - 50, 100, 100)]
            centers = [(x + w // 2, y + h // 2) for (x, y, w, h) in bounding_boxes]

            if len(centers) == 2:
                distance = int(math.sqrt((centers[0][0] - centers[1][0]) ** 2 + (centers[0][1] - centers[1][1]) ** 2))
                file_exists = os.path.isfile(output_csv)
                
                with open(output_csv, mode='a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    if not file_exists:
                        csv_writer.writerow(['Dyad Number', 'Trial Number', 'Second', 'X1', 'Y1', 'W1', 'H1', 'X2','Y2', 'W2', 'H2', 'Distance'])

                    csv_writer.writerow([self.dyad_number, trial_number, seconds, centers[0][0], centers[0][1], bounding_boxes[0][2], bounding_boxes[0][3], 
                                                 centers[1][0], centers[1][1], bounding_boxes[1][2], bounding_boxes[1][3], distance])

                for (x, y, w, h) in bounding_boxes:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                for center_x, center_y in centers:
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                cv2.line(frame, centers[0], centers[1], (255, 0, 0), 2)
                mid_x = (centers[0][0] + centers[1][0]) // 2
                mid_y = (centers[0][1] + centers[1][1]) // 2
                cv2.putText(frame, f"{distance}px", (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                self.draw_text_and_rectangle(width-250, height-15, frame, f"Second: {seconds}")
                self.draw_text_and_rectangle(width // 2 - 150, 30, frame, f"Dyad {self.dyad_number}, Trial {trial_number}") 

            out.write(frame)
            cv2.destroyWindow('Manual Selection')
            current_index += 1

        out.release()
        cap.release()
        cv2.destroyAllWindows()

    def mouse_callback_all(self, event, x, y, flags, param):
        points, status, first_face_confirmed, clicked = param
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked[0] = True

        if event == cv2.EVENT_RBUTTONDOWN:
            if len(points) > 0:
                print('HI')
                points.clear()
                status[0] = "Select first face"
                first_face_confirmed[0] = False
                clicked[0] = False

        if not first_face_confirmed[0]:
            if len(points) < 1:
                points.append((x, y))
            else:
                points[0] = (x, y)
        elif first_face_confirmed[0]:
            if len(points) < 2:
                points.append((x, y))
            else:
                points[1] = (x, y)


    def exit(self, out, cap, output_csv, output_vid, study_number):
        out.release()
        cap.release()
        cv2.destroyAllWindows()
        if os.path.exists(output_csv):
            os.remove(output_csv)
        if os.path.exists(output_vid):
            os.remove(output_vid)
        print(f"Succesfully exited and deleted progress for Dyad{study_number}")

    def analyze_per_face(self, input, use_one):
        input_csv = input
        input_vid = input_csv.replace(".csv", ".mp4").replace("_csv_", "_vid_")
        print(f"Loading input: {input_vid}")
        output_csv = input.replace("input", "processed").replace("manual_csv_", "").replace(f"dyad{self.dyad_number}", f"dyad{self.dyad_number}_manual_ipd")
        output_vid = output_csv.replace(".csv", "_vid.mp4")

        df = pd.read_csv(input_csv)
        trial_number = df['Trial Number'].iloc[0]

        cap = cv2.VideoCapture(input_vid)
        if not cap.isOpened():
            print("Error: Could not open video.")
            exit()

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_vid, fourcc, 1, (width, height))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        duration = total_frames / fps
        print(f"Manually calculating {duration} seconds")

        current_index = 0
        current_frame = 0
        points = [] # points[frame number][face number][X or Y]
        num_rows = len(df) # Number of outer list elements
        num_cols = 2  # Number of inner lists per outer element
        points = [[(0, 0, 0, 0) for _ in range(num_cols)] for _ in range(num_rows)]

        clicked = [False]

        while True: # First loop, going to evaluate each frame
            ret, frame = cap.read() 
            if not ret:
                print("End of first face processing")
                break
            clicked = [False]
            
            if pd.isna(df.loc[current_index, "X1"]) or not use_one:
                cv2.namedWindow(f'Manual Selection: Face {current_frame+1}')
                cv2.setMouseCallback(f'Manual Selection: Face {current_frame+1}', self.mouse_callback_per_face, (points, clicked, current_index, current_frame))
                
                while True:
                    temp_frame = frame.copy()
                    if points[current_index][0] != (0, 0, 0, 0):
                        x = points[current_index][0][0]
                        y = points[current_index][0][1]
                        w = points[current_index][0][2]
                        h = points[current_index][0][3]
                        cv2.rectangle(temp_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    self.draw_text_and_rectangle(10, height-15, temp_frame, "Select first face")
                    seconds = df['Second'].iloc[current_index]
                    self.draw_text_and_rectangle(width-250, height-15, temp_frame, f"Second: {seconds}")
                    self.draw_text_and_rectangle(width // 2 - 150, 30, temp_frame, f"Dyad {self.dyad_number}, Trial {trial_number}")

                    cv2.imshow(f'Manual Selection: Face {current_frame+1}', temp_frame)
                        
                    key = cv2.waitKey(1)
                    if key & clicked[0]:
                        break
                    elif key & 0xFF == ord('q'):
                        self.exit(out, cap, output_csv, output_vid, self.dyad_number)
                        return
                cv2.destroyWindow(f'Manual Selection: Face {current_frame+1}')
            elif use_one:
                x = int(df.loc[current_index, "X"])
                y = int(df.loc[current_index, "Y"])
                w = int(df.loc[current_index, "W"])
                h = int(df.loc[current_index, "H"])
                
                points[current_index][0] = (x, y, w, h)
            current_index += 1

        cv2.destroyAllWindows()
        current_index = 0
        current_frame = 1
        clicked[0] = False
        time.sleep(1.5)
        cap = cv2.VideoCapture(input_vid)
        if not cap.isOpened():
            print("Error: Could not open video.")
            exit()

        while True: # Second loop, going to evaluate each frame
            ret, frame = cap.read() 
            if not ret:   
                print("End of dyad processing")
                break

            clicked = [False]
        
            cv2.namedWindow(f'Manual Selection: Face {current_frame+1}')
            cv2.setMouseCallback(f'Manual Selection: Face {current_frame+1}', self.mouse_callback_per_face, (points, clicked, current_index, current_frame))
            
            while True:
                temp_frame = frame.copy()
                x = points[current_index][0][0]
                y = points[current_index][0][1]
                w = points[current_index][0][2]
                h = points[current_index][0][3]
                cv2.rectangle(temp_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                x = points[current_index][1][0]
                y = points[current_index][1][1]
                w = points[current_index][1][2]
                h = points[current_index][1][3]
                cv2.rectangle(temp_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                self.draw_text_and_rectangle(10, height-15, temp_frame, "Select second face")
                seconds = df['Second'].iloc[current_index]
                self.draw_text_and_rectangle(width-250, height-15, temp_frame, f"Second: {seconds}")
                self.draw_text_and_rectangle(width // 2 - 150, 30, temp_frame, f"Dyad {self.dyad_number}, Trial {trial_number}")

                cv2.imshow(f'Manual Selection: Face {current_frame+1}', temp_frame)
                    
                key = cv2.waitKey(1)
                # if key & 0xFF == 13:  # Enter key
                if key & clicked[0]:
                    break
                elif key & 0xFF == ord('q'):
                    self.exit(out, cap, output_csv, output_vid, self.dyad_number)
                    return

            # calculation shit
            bounding_boxes = [(points[current_index][0][0], points[current_index][0][1], points[current_index][0][2], points[current_index][0][3]),
                            (points[current_index][1][0], points[current_index][1][1], points[current_index][1][2], points[current_index][1][3])]
            centers = [(x + w // 2, y + h // 2) for (x, y, w, h) in bounding_boxes]

            if len(centers) == 2:
                distance = int(math.sqrt((centers[0][0] - centers[1][0]) ** 2 + (centers[0][1] - centers[1][1]) ** 2))
                file_exists = os.path.isfile(output_csv)

                with open(output_csv, mode='a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    if not file_exists:
                        csv_writer.writerow(['Dyad Number', 'Trial Number', 'Second', 'X1', 'Y1', 'W1', 'H1', 'X2','Y2', 'W2', 'H2', 'Distance'])

                    csv_writer.writerow([self.dyad_number, trial_number, seconds, centers[0][0], centers[0][1], bounding_boxes[0][2], bounding_boxes[0][3], 
                                                 centers[1][0], centers[1][1], bounding_boxes[1][2], bounding_boxes[1][3], distance])
                for (x, y, w, h) in bounding_boxes:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                for center_x, center_y in centers:
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                cv2.line(frame, centers[0], centers[1], (255, 0, 0), 2)
                mid_x = (centers[0][0] + centers[1][0]) // 2
                mid_y = (centers[0][1] + centers[1][1]) // 2
                cv2.putText(frame, f"{distance}px", (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

                self.draw_text_and_rectangle(width-250, height-15, frame, f"Second: {seconds}")
                self.draw_text_and_rectangle(width // 2 - 150, 30, frame, f"Dyad {self.dyad_number}, Trial {trial_number}")

            out.write(frame)
            cv2.destroyWindow(f'Manual Selection: Face {current_frame+1}')
            current_index += 1

        out.release()
        cap.release()
        cv2.destroyAllWindows()

    def mouse_callback_per_face(self, event, x, y, flags, param):
        points, clicked, current_index, current_frame = param
        if event == cv2.EVENT_RBUTTONDOWN and current_frame == 1:
            points[current_index][0] = (x, y, 100, 100)

        if event == cv2.EVENT_LBUTTONDOWN:
            clicked[0] = True

        points[current_index][current_frame] = (x, y, 100, 100)
    
    def draw_text_and_rectangle(self, x, y, frame, text):
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.25
        thickness = 4
        
        text_size, _ = cv2.getTextSize(text, font_face, font_scale, thickness)
        text_width, text_height = text_size

        text_org = (x, y)
        top_left = (x - 10, y - text_height - 10)
        bottom_right = (x + text_width + 10, y + 10)

        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 0), cv2.FILLED) # black rectangle
        cv2.putText(frame, text, text_org, font_face, font_scale, (255, 255, 255), thickness, cv2.LINE_AA) # white text

def process_file():
    path = "/Users/VHILab Core/Documents/FIDAC/Manual_Tracking"
    manu = Manual(path)
    study_num = 0
    manu.load_specific(study_num, analyze_type='per face', use_existing_one=False)

if __name__ == "__main__":
    process_file()