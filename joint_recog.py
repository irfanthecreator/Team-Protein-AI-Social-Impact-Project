import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Keeping the original DraggableDot logic, but adapting it for Streamlit
class DraggableDot:
    def __init__(self, x, y, tag):
        self.x = x
        self.y = y
        self.tag = tag

    def get_pos(self):
        return self.x, self.y

def getVec(d1: DraggableDot, d2: DraggableDot):
    x1, y1 = d1.get_pos()
    x2, y2 = d2.get_pos()
    return np.array([x2 - x1, y2 - y1])

def angle(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))
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

    if cos_sim < COS_SIM_THRESHOLD:
        danger = True
    elif y_ratio < KNEELING_RECOGNITION_THRESHOLD:
        danger = True
    else:
        danger = False

    return danger, cos_sim, angl, y_ratio

def update_plot(p1, p2, p3):
    fig, ax = plt.subplots()
    
    # Draw lines between points
    ax.plot([p1.x, p2.x], [p1.y, p2.y], marker='o', label='Line 1')
    ax.plot([p2.x, p3.x], [p2.y, p3.y], marker='o', label='Line 2')

    # Set the plot limits
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 400)

    # Labels
    ax.text(p1.x, p1.y, f"{p1.tag} ({p1.x}, {p1.y})", fontsize=9, ha='right')
    ax.text(p2.x, p2.y, f"{p2.tag} ({p2.x}, {p2.y})", fontsize=9, ha='right')
    ax.text(p3.x, p3.y, f"{p3.tag} ({p3.x}, {p3.y})", fontsize=9, ha='right')

    ax.legend()
    st.pyplot(fig)

def main():
    st.title('Draggable Dots Simulation (via Sliders)')

    # Initialize positions using sliders
    p1_x = st.slider('P1 X', 0, 400, 100)
    p1_y = st.slider('P1 Y', 0, 400, 100)
    p2_x = st.slider('P2 X', 0, 400, 200)
    p2_y = st.slider('P2 Y', 0, 400, 200)
    p3_x = st.slider('P3 X', 0, 400, 300)
    p3_y = st.slider('P3 Y', 0, 400, 100)

    # Create DraggableDot objects with these positions
    p1 = DraggableDot(p1_x, p1_y, "p1")
    p2 = DraggableDot(p2_x, p2_y, "p2")
    p3 = DraggableDot(p3_x, p3_y, "p3")

    # Calculate vectors and angles
    vec12 = getVec(p1, p2)
    vec23 = getVec(p2, p3)

    danger, cos_sim, angl, y_ratio = isDangerPose(vec12, vec23)

    st.write(f"Cosine Similarity: {cos_sim:.3f}")
    st.write(f"Angle between lines: {angl:.2f} degrees")
    st.write(f"Y Ratio: {y_ratio:.3f}")
    st.write(f"Pose Danger: {'Yes' if danger else 'No'}")

    # Update the plot
    update_plot(p1, p2, p3)

if __name__ == "__main__":
    main()
