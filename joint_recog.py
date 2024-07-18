import tkinter as tk
import numpy as np


class DraggableDot:
    def __init__(self, canvas, x, y, tag):
        self.canvas = canvas
        self.tag = tag
        self.id = canvas.create_oval(x-7.5, y-7.5, x+7.5, y+7.5, fill="black", tags=tag)  # Larger oval size
        self.text_id = canvas.create_text(x, y+15, text=f"{self.tag} ({x}, {y})", anchor="center")  # Text label below the dot
        self.x = x
        self.y = y
        self.drag_data = {"x": 0, "y": 0}
        
        self.canvas.tag_bind(self.tag, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.on_motion)
        self.canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.on_release)
    
    def on_press(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
    
    def on_motion(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        self.canvas.move(self.tag, dx, dy)
        self.canvas.move(self.text_id, dx, dy)  # Move the text label along with the dot
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
        self.x += dx
        self.y += dy
        self.update_position_text()
        update_lines()
    
    def on_release(self, event):
        # Ensure the dot stays within canvas bounds
        self.x = min(max(self.x, 7.5), self.canvas.winfo_width() - 7.5)
        self.y = min(max(self.y, 7.5), self.canvas.winfo_height() - 7.5)
        self.canvas.coords(self.id, self.x-7.5, self.y-7.5, self.x+7.5, self.y+7.5)
        self.update_position_text()
        update_lines()
    
    def update_position_text(self):
        self.canvas.itemconfig(self.text_id, text=f"{self.tag} ({self.x}, {self.y})")

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
    # Ensure cos_theta is within [-1, 1] to avoid domain errors
    angle_deg = np.degrees(angle_rad)
    
    return angle_deg

#############################################################
def isDangerPose(vec1, vec2):
    COS_SIM_THRESHOLD = -0.5
    KNEELING_RECOGNITION_THRESHOLD = 0.3

    s1 = np.linalg.norm(vec1)
    s2 = np.linalg.norm(vec2)
    dy1 = vec1[1]
    dy2 = vec2[1]
    y_ratio = abs(dy2 / dy1 if dy1 != 0 else 0)

    # -1 <= cos_sim <= 1
    cos_sim = vec1.dot(vec2) / s1 / s2
    angl = angle(-vec1, vec2)

    # if knee is over-bended (close to -1)
    if cos_sim < COS_SIM_THRESHOLD:
        danger = True
    
    # if dy is too small (ex. kneeling)
    elif y_ratio < KNEELING_RECOGNITION_THRESHOLD:
        danger = True
    
    else:
        danger = False

    print("cos_sim: {}, angle: {}, y_ratio: {}, danger: {}"\
        .format(cos_sim, angl, y_ratio, danger))

    return danger

#############################################################
    
def update_lines():
    global vec12, vec23
    canvas.coords(line1, p1.x, p1.y, p2.x, p2.y)
    canvas.coords(line2, p2.x, p2.y, p3.x, p3.y)

    vec12 = getVec(p1, p2)
    vec23 = getVec(p2, p3)
    
    danger = isDangerPose(vec12, vec23)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Movable Dots")

    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    p1 = DraggableDot(canvas, 100, 100, "p1")
    p2 = DraggableDot(canvas, 200, 200, "p2")
    p3 = DraggableDot(canvas, 300, 100, "p3")

    vec12 = getVec(p1, p2)
    vec23 = getVec(p2, p3)

    line1 = canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="black")
    line2 = canvas.create_line(p2.x, p2.y, p3.x, p3.y, fill="black")

    root.mainloop()
