''' THIS IS FOR FIDAC '''

from imports import *
from pyfeat_detector import PyFeat_Detection

import logging
logging.getLogger().setLevel(logging.ERROR) # this is to prevent py-feat's NO FACE DETECTED error, which doesn't matter

# Code that runs py-feat or other libraries

# need to consider best way to set up build 

# also add total seconds (i.e. Second: 23/156)

class Distance:
    '''
    Each distance object is a specific trial (i.e. trial 1 or trial2) of a specific study
    '''

    def __init__(self, input):
        self.video_path = input

    def compute_distance(self, num_faces=2, second_frequency=1, detection_model='py-feat', optimize=False):
        '''
        Determines location of faces, computes and stores interpersonal distance, loads manual frames.
        Currently utlizies py-feat's Detector with a face_thershold of .9
        '''
        ''' add check to see if dyad file in file is same as the folder'''
        self.study_number = int(''.join(filter(str.isdigit, os.path.basename(self.video_path).split('_')[0][4:]))) # determines study_number from string manipulation
        self.trial_number = 1 if 'trial1' in self.video_path else 2 # gets trial number
        self.num_faces = num_faces
        ''' need to change trial so it fits however many the user wants'''

        input_video_path = self.video_path
        core_folder = input_video_path.split('/Input/')[0]

        video_output_path = f'{core_folder}/Processed/dyad{self.study_number}/video_dyad{self.study_number}_trial{self.trial_number}.mp4'
        temp_frame_path = core_folder + '/temp_frame.jpg'
        csv_output_path = video_output_path.replace("video_", "csv_").replace(".mp4", ".csv")

        print(f"Calculating distance from: {input_video_path}")
        if os.path.exists(video_output_path) and not optimize: # check if already exists
            override = input("File already processed: Override? (y/n): ")
            if override == "n" or override == "no":
                return
            
        # set up the model to use for detection
        if detection_model == 'py-feat': 
            print("Using py-feat")
            model = PyFeat_Detection()
        elif detection_model == 'mediapipe': 
            print("Using mediapipe")
            from mediapipe_detector import MediaPipe_Detection
            model = MediaPipe_Detection()
        else:
            print("Incorrect model selected")

        # important frame information captured by cv2
        cap = cv2.VideoCapture(input_video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = int(total_frames / fps)

        # output_video, which is at 1 frame per second
        out = cv2.VideoWriter(video_output_path, fourcc, 1, (width, height)) 

        frame_count = 0 # current frame on
        distance = None # distance between faces
        manual_frames = [] # list of frames not detected, saved as (second, frame)
        manual_values = [] # info about manual frames, saved as (second, x, y, w, h)
        seconds_tracked = []

        if optimize and os.path.exists(video_output_path):
            # saves the path to a csv and video path created as temp files
            csv_old, video_path_old = setup_prev_model()

        with open(csv_output_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            if detection_model != 'mediapipe': pbar = tqdm(total=duration)
           
            # x, y are the points' center
            headers = ['Study Number', 'Trial Number', 'Second']
            for i in range(1, num_faces + 1):
                headers.extend([f'X{i}', f'Y{i}', f'W{i}', f'H{i}'])
            headers.append('Distance')
            csv_writer.writerow(headers) # first row output

            if optimize:
                # adds previous values to the CSV
                self.csv_add_prev_values()

            while cap.isOpened(): # iterates through each frame
                ret, frame = cap.read()
                if not ret:
                    if optimize:
                        self.vid_add_prev_values()
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                
                if frame_count % int(fps / second_frequency) == 0: # only evaluates a certain amount of times
                    if detection_model != 'mediapipe': pbar.update(1)
                    seconds = frame_count // fps
                    centers = [] # center of face, stored as (x, y)

                    # creates a temporary frame and detects faces on that
                    cv2.imwrite(temp_frame_path, frame)

                    filtered_detections, bounding_boxes = model.calculate_bounding_box(temp_frame_path, num_faces)

                    if len(bounding_boxes) == num_faces: # only stores in csv if exact amt of faces
                        centers = [(x + w // 2, y + h // 2) for (x, y, w, h) in bounding_boxes]
                        distance = int(math.sqrt((centers[0][0] - centers[1][0]) ** 2 + (centers[0][1] - centers[1][1]) ** 2))
                        csv_writer.writerow([self.study_number, self.trial_number, seconds, centers[0][0], centers[0][1], bounding_boxes[0][2], bounding_boxes[0][3], 
                                                centers[1][0], centers[1][1], bounding_boxes[1][2], bounding_boxes[1][3], distance])
                        seconds_tracked.append(seconds)
                    # change this        
                    elif len(filtered_detections) == 1: # if only one face is detected, appends to manual_values
                        for x, y, w, h in bounding_boxes:
                            manual_values.append((seconds, x, y, w, h))
                        manual_frames.append((frame, seconds))
                        bounding_boxes.clear()
                    else:
                        manual_frames.append((frame, seconds))

                    # draws boxes around faces
                    for (x, y, w, h) in bounding_boxes: 
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    if len(centers) == 2 and distance is not None:
                        # draw dots around center of face and line connecting them with distance in pixels written
                        for x, y in centers:
                            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
                        cv2.line(frame, centers[0], centers[1], (255, 0, 0), 2)
                        x_mid = (centers[0][0] + centers[1][0]) // 2
                        y_mid = (centers[0][1] + centers[1][1]) // 2
                        cv2.putText(frame, f"{distance}px", (x_mid, y_mid), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

                        # output seconds and dyad information
                        self.draw_text_and_rectangle(width-250, height-15, frame, f"Second: {seconds}")
                        self.draw_text_and_rectangle(width // 2 - 150, 30, frame, f"Study {self.study_number}, Trial {self.trial_number}")

                        out.write(frame)

                frame_count += 1
            if detection_model != 'mediapipe': pbar.close()
        
        self.create_manual_video(manual_frames, manual_values)

        out.release()
        cap.release()
        cv2.destroyAllWindows()

        os.remove(temp_frame_path)

    def draw_text_and_rectangle(self, x, y, frame, text):
        '''
        Draws text at specified x,y location on a specific frame.
        Based on length of text (in white), draws a black rectangle surroudning it
        '''
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

    def setup_prev_model(self):
        '''
        Creates a temporary csv and video with the output from the previous model
        
        '''
        pass


    def csv_add_prev_values(self):
        '''
        adds the saved input_values from the old model and merges with new model's output
        sorts through them and delets overlaps (favors new model?)
        '''
        pass
    
    def vid_add_prev_values(self):
        '''
        adds the saved video frames from the old model to the new model. doesn't care about sorting
        '''
        pass

    def create_manual_video(self, manual_frames, manual_values):
        '''
        Creates csv and video of all manual frames that need to be human-coded.

        Key variables:

        '''
        
        # create manual file
        core_folder = self.video_path.split('/Input/')[0]
        manual_path = core_folder + '/Manual_Tracking'
        os.makedirs(manual_path + '/input', exist_ok=True)
        os.makedirs(manual_path + '/processed', exist_ok=True)

        csv_manual_path = f'{manual_path}/input/manual_csv_dyad{self.study_number}_trial{self.trial_number}.csv'
        video_manual_path = csv_manual_path.replace("_csv", "_vid").replace(".csv", '.mp4')

        if not manual_frames: # checks if no frames to add manually
            print("No manual frames")
            return
        
        height, width, layers = manual_frames[0][0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        
        video = cv2.VideoWriter(video_manual_path, fourcc, 1, (width, height)) # 1 frame per second
        
        # opens new file, removing the one that currently exists
        with open(csv_manual_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            m_headers = ['Study Number', 'Trial Number', 'Second']
            for i in range(1, self.num_faces):
                m_headers.extend([f'X{i}', f'Y{i}', f'W{i}', f'H{i}'])
            csv_writer.writerow(m_headers)

            '''
            Iterates through each frame in manual_frames, noting the current second. It then loops through 
            manual values, and if that second is also apparant in manual values, the row includes: x, y, w, h.
            If not, it just includes the study_number, trial_number, and second
            '''
            for frame, second in manual_frames:
                found = False
                for sec, x, y, w, h in manual_values:
                    if sec == second:
                        csv_writer.writerow([self.study_number, self.trial_number, second, x, y, w, h])
                        found = True
                if not found:
                    csv_writer.writerow([self.study_number, self.trial_number, second])

                # output seconds and dyad information
                self.draw_text_and_rectangle(width-250, height-15, frame, f"Second: {second}")
                self.draw_text_and_rectangle(width // 2 - 150, 30, frame, f"Study {self.study_number}, Trial {self.trial_number}")
                video.write(frame) 
        video.release()

def process_file(num, model, opt):
    core_path = f'/Users/VHILab Core/Documents/FIDAC' # this needs to be changed per user

    input_path = core_path + f'/Input/dyad{num}/'
    os.makedirs(input_path.replace("Input", "Processed"), exist_ok=True)

    if not os.path.exists(input_path):
        print(f"'{input_path}' does not exist.")
    else:
        for filename in os.listdir(input_path):
            if filename.lower().endswith(".mp4") and "center" in filename.lower():
                name = input_path + filename
                dist = Distance(name) # name includes everything till the file
                dist.compute_distance(optimize, detection_model=model, optimize=opt)

def rename_file(file_path):
    directory, original_file_name = os.path.split(file_path)
    new_file_name = original_file_name.lower().replace(" ", "_")
    new_file_path = os.path.join(directory, new_file_name)
    os.rename(file_path, new_file_path)
    return new_file_path

if __name__ == "__main__":
    optimize = False
    if len(sys.argv) == 3:
        study_num = int(sys.argv[1])
        model_type = sys.argv[2]
    if len(sys.argv) > 3:
        if sys.argv[3] == "optimize": optimize = True

    process_file(study_num, model_type, optimize)