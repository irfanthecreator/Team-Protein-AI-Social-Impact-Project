import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# DraggableDot equivalent for setting positions via sliders
class DraggableDot:
    def __init__(self, x, y, tag):
        self.x = x
        self.y = y
        self.tag = tag

    def get_pos(self):
        return self.x, self.y

# Vector calculation functions
def getVec(d1: DraggableDot, d2: DraggableDot):
    x1, y1 = d1.get_pos()
    x2, y2 = d2.get_pos()

    return np.array([x2 - x1, y2 - y1])

def angle(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))  # Clip to prevent domain errors
    angle_deg = np.degrees(angle_rad)

    return angle_deg

def isDangerPose(vec1, vec2):
    COS_SIM_THRESHOLD = -0.5
    KNEELING_RECOGNITION_THRESHOLD = 0.3

    s1 = np.linalg.norm(vec1)
    s2 = np.linalg.norm(vec2)
    dy1 = vec1[1]
    dy2 = vec2[1]
    y_ratio = abs(dy2 / dy1 if dy1 != 0 else 0)

    cos_sim = vec1.dot(vec2) / s1 / s2
    angl = angle(-vec1, vec2)

    if cos_sim < COS_SIM_THRESHOLD or y_ratio < KNEELING_RECOGNITION_THRESHOLD:
        danger = True
    else:
        danger = False

    st.write(f"cos_sim: {cos_sim}, angle: {angl}, y_ratio: {y_ratio}, danger: {danger}")
    
    return danger

# Streamlit user inputs for moving dots
st.title("Move the Dots and Check the Pose")
x1 = st.slider("p1 x-coordinate", 0, 400, 100)
y1 = st.slider("p1 y-coordinate", 0, 400, 100)
x2 = st.slider("p2 x-coordinate", 0, 400, 200)
y2 = st.slider("p2 y-coordinate", 0, 400, 200)
x3 = st.slider("p3 x-coordinate", 0, 400, 300)
y3 = st.slider("p3 y-coordinate", 0, 400, 100)

# Create draggable dots
p1 = DraggableDot(x1, y1, "p1")
p2 = DraggableDot(x2, y2, "p2")
p3 = DraggableDot(x3, y3, "p3")

# Plot the points and lines
fig, ax = plt.subplots()
ax.plot([p1.x, p2.x], [p1.y, p2.y], 'k-', lw=2)
ax.plot([p2.x, p3.x], [p2.y, p3.y], 'k-', lw=2)
ax.plot(p1.x, p1.y, 'ro', label="p1")
ax.plot(p2.x, p2.y, 'go', label="p2")
ax.plot(p3.x, p3.y, 'bo', label="p3")
ax.set_xlim([0, 400])
ax.set_ylim([0, 400])
ax.invert_yaxis()  # To match typical canvas behavior
ax.legend()

st.pyplot(fig)

# Vector calculations and pose check
vec12 = getVec(p1, p2)
vec23 = getVec(p2, p3)

danger = isDangerPose(vec12, vec23)
