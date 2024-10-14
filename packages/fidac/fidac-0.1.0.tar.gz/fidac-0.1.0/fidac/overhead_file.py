import subprocess
path = "/Users/VHILab Core/Documents/FIDAC/Programs/measure_position.py"
subprocess.run(["python", path, "300", "py-feat"])
subprocess.run(["python", path, "300", "mediapipe", "optimize"])

'''
Mediapipe: 3, 4, 8, 9, 11, 13, 14
py-feat: got 7 right but missing 11

'''