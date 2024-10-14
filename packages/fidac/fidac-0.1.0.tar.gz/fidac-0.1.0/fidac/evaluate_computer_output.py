
'''
Similar to manual_calculate, this file goes through a set of outputed models and plays them back relatively fast.
Users then have the option of pressing enter for the next or R to continue to the next video
'''
from imports import *


class Eval_Output:
    def process_output(self, path, dyad_num, trial_num):
        '''
        Write code that opens a video, whose path is stored in the variable 'path'. 
        The video is saved in 1 fps but I want to play it faster, so make it by default 10 fps and have the speed saved in an adjustable variable.
        If the user presses space, the video pauses and if they press it again it plays. Add some text in the bottom that says "Press space to play/pause". 
        After the video is complete, text should appear on the video (in the middle) saying: "Repeat (r) or End (enter)". If the user presses r,
        the video repeats but this time is in the original 1 fps speed. If they press enter, then the video closes
        '''
        video = cv2.VideoCapture(path)
        if not video.isOpened():
            print("Error: Could not open video.")
            exit()

        # playback speeds
        original_fps = 1
        playback_fps = 5
        current_fps = playback_fps

        # Playback control variables
        paused = True 
        started = False

        ret, frame = video.read()
        if not ret:
            print("Error: Could not read the first frame of the video.")
            exit()

        self.display_text(frame, "Press 's' to start", (50, int(video.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2)), scale=1.5)
        cv2.imshow('Video Playback', frame)

        while True:
            # Wait for the user to press 's' to start the video
            if not started:
                key = cv2.waitKey(0)
                if key == ord('s'):
                    started = True
                    paused = False
                elif key == ord('q'):
                    break
                continue

            if not paused:
                ret, frame = video.read()
                if not ret:
                    # End of video
                    if frame_prev is not None:
                        # Use the last frame to display repeat/exit options
                        frame = frame_prev.copy()
                        self.display_text(frame, "Repeat (r) or End (q)", (50, int(video.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2)), scale=1.5)
                        cv2.imshow('Video Playback', frame)
                        
                        key = cv2.waitKey(0)  # Wait for user input
                        if key == ord('r'):
                            print(f"Flagging dyad {dyad_num} trial {trial_num}")
                            current_fps = original_fps
                            video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
                        elif key == ord('q'): 
                            break
                    else:
                        print("Error: No frames available to display.")
                        break
                    continue

                frame_prev = frame.copy()  # Save last frame to use when the video ends
                self.display_text(frame, "Press space to play/pause", (10, int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) - 20))
                cv2.imshow('Video Playback', frame)

            key = cv2.waitKey(int(1000 / current_fps))

            if key == ord(' '):  # Space bar to pause/play
                paused = not paused
            elif key == ord('q'):  # Quit the video if 'q' is pressed
                break

        video.release()
        cv2.destroyAllWindows()


    # Function to display text on frame\
    def display_text(self, frame, text, position, scale=1, color=(255, 255, 255)):
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, 2)
        text_width, text_height = text_size

        x, y = position
        box_coords = ((x, y - text_height - 10), (x + text_width + 10, y + 10))

        cv2.rectangle(frame, box_coords[0], box_coords[1], (0, 0, 0), cv2.FILLED)
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2, cv2.LINE_AA)

def process_file():
    study_range = [2, 10]
    for study in range(study_range[0], study_range[1]+1):
        if study != 4:
            for trial_num in range (1, 3): 
                path = f'/Users/VHILab Core/Documents/VHIL_E2E_Test/Output/dyad{study}/ipd_video_trial{trial_num}.mp4'
                eval = Eval_Output()
                eval.process_output(path, study, trial_num)


if __name__ == "__main__":
    process_file()