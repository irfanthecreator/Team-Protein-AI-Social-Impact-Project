import openvino as ov
import numpy as np
import matplotlib.pyplot as plt
import cv2
# custom module
import model_const as con
from joint_recog import isDangerPose as _isDangerPose

PATHS = {
    "FP16": {
        "bin": r"Team-Protein-AI-Social-Impact-Project\intel\human-pose-estimation-0007\FP16\human-pose-estimation-0007.bin",
        "xml": r"Team-Protein-AI-Social-Impact-Project\intel\human-pose-estimation-0007\FP16\human-pose-estimation-0007.xml",
    },
    "FP32": {
        "bin": r"Team-Protein-AI-Social-Impact-Project\intel\human-pose-estimation-0007FP32\human-pose-estimation-0007.bin",
        "xml": r"Team-Protein-AI-Social-Impact-Project\intel\human-pose-estimation-0007\FP32\human-pose-estimation-0007.xml",
    }
}

class PosDetection(object):
    __instance = None
    threshold = 0.01

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
    
    def __init__(self):
        self.core = ov.Core()
        self.model_init()

    def model_init(self, precision="FP32"):
        if precision == "FP32":
            self.model_path = PATHS["FP32"]["xml"]
        else:
            self.model_path = PATHS["FP16"]["xml"]

        self.model = self.core.read_model(model=self.model_path)
        self.compiled_model = self.core.compile_model(model=self.model, device_name="CPU")

        self.input_layer = self.compiled_model.input(0)
        self.output_layer = self.compiled_model.output(0)
        # input size: [1,3,448,448]
        # output size: [1,17,224,224]
        
        N, input_channels, self.input_height, self.input_width \
            = self.input_layer.shape

    def get_input_size(self):
        return self.input_width, self.input_height
    
    def resize(self, cv2_image):
        w, h = self.get_input_size()
        resized_image: cv2.typing.MatLike = cv2.resize(cv2_image, (w, h))
        transposed_image = resized_image.transpose(2, 0, 1)
        # OpenCV img = cv2.imread(path) loads an image with HWC-layout (height, width, channels),
        # while Pytorch requires CHW-layout.
        # So we have to do np.transpose(image,(2,0,1)) for HWC->CHW transformation.
        
        # array dimension size [3,448,448] -> [1,3,448,448]
        input_array = np.expand_dims(transposed_image, 0)

        return input_array
    
    def predict(self, cv2_image: cv2.typing.MatLike) -> list[tuple[int, int] | None]:
        arr = self.resize(cv2_image)
        h, w, _= cv2_image.shape
        # running the model
        # results: 4D numpy array (1, 17, 224, 224)
        results = self.compiled_model([arr])[self.output_layer]

        points = []
        for i in range(17):
            heatmap = results[0][i]
            _, confidence, _, point = cv2.minMaxLoc(heatmap)
            
            # relative position on input layer image
            x = point[0] / heatmap.shape[1]
            y = point[1] / heatmap.shape[0]

            img_pos = int(w * x), int(h* y)
            points.append(img_pos if confidence > self.threshold else None)
        
        # list of tuple, which is a position of each joint
        # None represents the joint is not found in the image
        return points
    
    def setModelPrecision(self, precision):
        print(precision)
        self.model_init(precision)

# showing results on image
def getRadius(img):
    # To make dots visible on any size of the image,
    # dot radius is 0.5% of image size
    h, w, _ = img.shape
    m = min(h, w)
    radius = m // 200
    if radius < 1: radius = 1
    return radius

def drawCircle(img, points, color: tuple[int, int, int]):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    radius = getRadius(img)
    for point in points:
        if point is not None:
            cv2.circle(img, point, radius, color, thickness=-1, lineType=cv2.FILLED)

    return img

def drawLines(img, points, color: tuple[int, int, int]):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    radius = getRadius(img)
    radius = 10
    for i, start_point in enumerate(points):
        if start_point is None:
            continue

        for j in con.CONNECTIONS[i]:
            end_point = points[j]
            if end_point is not None:
                cv2.line(img, start_point, end_point, color, thickness=radius)
        
    return img

def isDangerPose(points: list[tuple[int, int] | None]):
    temp = False
    for side in ("left", "right"):
        hip_idx = con.JOINT_NAME.index(f"{side}_hip")
        knee_idx = con.JOINT_NAME.index(f"{side}_knee")
        ankle_idx = con.JOINT_NAME.index(f"{side}_ankle")

        p1 = points[hip_idx]
        p2 = points[knee_idx]
        p3 = points[ankle_idx]

        if None in (p1, p2, p3):
            continue

        # 2d vector p1->p2
        v1 = np.array([p2[0] - p1[0], p2[1] - p1[1]])
        # 2d vector p2->p3
        v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
        temp = temp or _isDangerPose(v1, v2)

    # if any of both sides has danger pose, danger = True
    return temp

def __main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error")
        return
    
    pd = PosDetection()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        points = pd.predict(frame)
        danger = isDangerPose(points)
        print("danger: {}".format(
            danger
        ))
        if danger:
            color = (255, 0, 0)  # red
        else:
            color = (0, 255, 0)  # green
        
        result_img = drawLines(frame, points, color)
        cv2.imshow("Name", cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    __main()
