JOINT_NAME = [
    "nose", "left_eye",
    "right_eye", "left_ear",
    "right_ear", "left_shoulder",
    "right_shoulder", "left_elbow",
    "right_elbow", "left_wrist",
    "right_wrist", "left_hip",
    "right_hip", "left_knee",
    "right_knee", "left_ankle",
    "right_ankle"
] # 0 to 16
CONNECTIONS = {
    0: [1, 2],       # nose connected to left_eye, right_eye
    1: [0, 3],       # left_eye connected to nose, left_ear
    2: [0, 4],       # right_eye connected to nose, right_ear
    3: [1, 5],       # left_ear connected to left_eye, left_shoulder
    4: [2, 6],       # right_ear connected to right_eye, right_shoulder
    5: [3, 6, 7, 11],# left_shoulder connected to left_ear, right_shoulder, left_elbow, left_hip
    6: [4, 5, 8, 12],# right_shoulder connected to right_ear, left_shoulder, right_elbow, right_hip
    7: [5, 9],       # left_elbow connected to left_shoulder, left_wrist
    8: [6, 10],      # right_elbow connected to right_shoulder, right_wrist
    9: [7],          # left_wrist connected to left_elbow
    10: [8],         # right_wrist connected to right_elbow
    11: [5, 12, 13], # left_hip connected to left_shoulder, right_hip, left_knee
    12: [6, 11, 14], # right_hip connected to right_shoulder, left_hip, right_knee
    13: [11, 15],    # left_knee connected to left_hip, left_ankle
    14: [12, 16],    # right_knee connected to right_hip, right_ankle
    15: [13],        # left_ankle connected to left_knee
    16: [14]         # right_ankle connected to right_knee
}

# written by ChatGPT

