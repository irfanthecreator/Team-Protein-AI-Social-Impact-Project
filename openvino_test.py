import openvino as ov
import numpy as np
import matplotlib.pyplot as plt
import cv2

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
] # 0 to 17

def resize_image(image, input_width, input_height):
    resized_image = cv2.resize(image, (input_width, input_height))
    transposed_image = resized_image.transpose(2, 0, 1)
    input_image = np.expand_dims(transposed_image, 0)

    return input_image, resized_image
    
def __main():
    core = ov.Core()

    model = core.read_model(model="model/human-pose-estimation-0007.xml")
    compiled_model = core.compile_model(model=model, device_name="CPU")

    input_layer = compiled_model.input(0)
    output_layer = compiled_model.output(0)

    # [1,3,448,448] [1,17,224,224]
    print(input_layer.shape, output_layer.shape)

    # load image
    image = cv2.imread("img/t3.jpg")
    N, input_channels, h, w = input_layer.shape
    input_image, resized_image = resize_image(image, w, h)

    # 4D numpy array (1, 17, 224, 224)
    results = compiled_model([input_image])[output_layer]
    threshold = 0.1
    points = []
    for i in range(17):
        heatmap = results[0][i]
        _, conf, _, point = cv2.minMaxLoc(heatmap)
        x = (w * point[0]) / heatmap.shape[1]
        y = (h * point[1]) / heatmap.shape[0]
        points.append((int(x), int(y)) if conf > threshold else None)

    # Draw points on the image
    for point in points:
        if point is not None:
            cv2.circle(resized_image, point, 4, (0, 255, 0), thickness=-1, lineType=cv2.FILLED)

    plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
    plt.show()
    quit()

    confidence_threshold = 0.95
    face_boxes, scores = find_faceboxes(image, results, confidence_threshold)
    print(face_boxes)
if __name__ == "__main__":
    __main()