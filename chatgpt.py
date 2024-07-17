import cv2
import numpy as np
from openvino.inference_engine import IECore

# Initialize the Inference Engine
ie = IECore()

# Load the network
model_path = "human-pose-estimation-0007.xml"
net = ie.read_network(model=model_path, weights=model_path.replace(".xml", ".bin"))
exec_net = ie.load_network(network=net, device_name="CPU")

# Prepare input blob
input_blob = next(iter(net.input_info))
output_blob = next(iter(net.outputs))

# Read and preprocess an input image
image_path = "input.jpg"
image = cv2.imread(image_path)
initial_h, initial_w = image.shape[:2]

# The model expects BGR input of shape [1x3x256x456]
input_height, input_width = net.input_info[input_blob].input_data.shape[2:]
image_resized = cv2.resize(image, (input_width, input_height))
image_transposed = image_resized.transpose((2, 0, 1))  # Change data layout from HWC to CHW
input_data = np.expand_dims(image_transposed, axis=0)

# Perform inference
results = exec_net.infer(inputs={input_blob: input_data})

# Extract results
keypoints = results[output_blob][0]

# Keypoints mapping to body parts
body_parts = [
    "nose", "neck", "right shoulder", "right elbow", "right wrist",
    "left shoulder", "left elbow", "left wrist", "right hip", "right knee",
    "right ankle", "left hip", "left knee", "left ankle", "right eye",
    "left eye", "right ear", "left ear"
]

# Process and draw the results
threshold = 0.5
for i, (x, y, confidence) in enumerate(keypoints):
    if confidence > threshold:
        x = int(x * initial_w)
        y = int(y * initial_h)
        cv2.circle(image, (x, y), 3, (0, 255, 0), thickness=-1, lineType=cv2.FILLED)
        cv2.putText(image, body_parts[i], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Display the output
cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
