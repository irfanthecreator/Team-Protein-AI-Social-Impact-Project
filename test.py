import cv2
import numpy as np
from openvino.runtime import Core

# Initialize OpenVINO Runtime
ie = Core()

# Load the network and corresponding weights from file
model_path = "model/human-pose-estimation-0007.xml"
weights_path = "model/human-pose-estimation-0007.bin"
network = ie.read_model(model=model_path, weights=weights_path)
exec_net = ie.compile_model(network, device_name="CPU")

# Get input and output layers
input_layer = next(iter(exec_net.inputs))
output_layer = next(iter(exec_net.outputs))

# Load and preprocess the image
image_path = "img/t1.jpg"
frame = cv2.imread(image_path)
initial_h, initial_w = frame.shape[:2]
input_blob = cv2.resize(frame, (256, 456))  # Model expects 256x456 input
input_blob = input_blob.transpose((2, 0, 1))  # Change data layout from HWC to CHW
input_blob = np.expand_dims(input_blob, axis=0)  # Add batch dimension

# Perform inference
results = exec_net([input_blob])[output_layer]

# Process the results
threshold = 0.1
points = []
for i in range(18):
    heatmap = results[0, i, :, :]
    _, conf, _, point = cv2.minMaxLoc(heatmap)
    x = (initial_w * point[0]) / heatmap.shape[1]
    y = (initial_h * point[1]) / heatmap.shape[0]
    points.append((int(x), int(y)) if conf > threshold else None)

# Draw points on the image
for point in points:
    if point is not None:
        cv2.circle(frame, point, 5, (0, 255, 0), thickness=-1, lineType=cv2.FILLED)

# Display the image with keypoints
cv2.imshow("Pose Estimation", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()