"""
To run the code, type "streamlit run streamlit_ui.py"

"""

import streamlit as st
import cv2
from PIL import Image
import io
import numpy as np
# custom module
import model_pose


st.set_page_config(page_title="AI-Powered Posture Monitoring", page_icon="👴", layout="wide")

def main():
    st.title("AI-Powered Posture Monitoring for Elderly Care")
    st.write("Our project aims to enhance the quality of life for elderly individuals with osteoporosis and poor posture by developing an AI-powered posture monitoring and rehabilitation system. Utilizing the human-pose-estimation-0007 model from OpenVINO, our system provides real-time feedback to correct posture, helping to prevent fractures and improve mobility.")
    
    # Confidence threshold and model precision settings
    confidence_threshold = st.sidebar.slider("Select the Confidence Threshold for Detection", 10, 100, 50)
    model_selector = st.sidebar.radio("Model Precision", ('FP16', 'FP32'), index=0)

    # Create tabs for Video and Webcam
    tab1, tab2, tab3 = st.tabs(["Live Camera Feed", "Video Upload", "Photo Analysis"])

    with tab1:
        st.header("Live Posture Monitoring")
        st.write("This section could potentially display a live video feed from your webcam with real-time posture analysis.")
        
        # Toggle to start/stop webcam
        if st.button('Start Webcam'):
            # Starting the webcam feed
            cap = cv2.VideoCapture(0)  # 0 for default camera
            run = True
            pose_detector = model_pose.PosDetection()
            pose_detector.setModelPrecision(model_selector)

            while run:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to capture video.")
                    break
                # Pose prediction
                points = pose_detector.predict(frame)
                frame = model_pose.drawCircle(frame, points, (255, 0, 0))
                frame = model_pose.drawLines(frame, points, (0, 255, 0))
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st.image(frame)
                
                if st.button('Stop Webcam'):
                    run = False
            cap.release()

    with tab2:
        st.header("Video Upload for Posture Analysis")
        st.write("Upload a video file to analyze posture over time.")
        uploaded_video = st.sidebar.file_uploader("Choose a video file", type=['mp4', 'avi'], key='video')
        
        if uploaded_video is not None:
            cap = cv2.VideoCapture(uploaded_video.name)
            pose_detector = model_pose.PosDetection()
            pose_detector.setModelPrecision(model_selector)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                points = pose_detector.predict(frame)
                frame = model_pose.drawCircle(frame, points, (255, 0, 0))
                frame = model_pose.drawLines(frame, points, (0, 255, 0))
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st.image(frame)
                if st.sidebar.button("Stop Video"):
                    break
            cap.release()

    with tab3:
        st.header("Upload Photo for Posture Analysis")
        uploaded_photo = st.sidebar.file_uploader("Choose an image file", type=['jpg', 'png', 'jpeg'], key='photo')
        
        if uploaded_photo is not None:
            bytes_data = uploaded_photo.read()
            image = Image.open(io.BytesIO(bytes_data))
            image = np.array(image)
            image = image[:, :, ::-1]  # Convert RGB to BGR for OpenCV processing
            pose_detector = model_pose.PosDetection()
            pose_detector.setModelPrecision(model_selector)
            points = pose_detector.predict(image)
            image = model_pose.drawCircle(image, points, (255, 0, 0))
            image = model_pose.drawLines(image, points, (0, 255, 0))
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            st.image(image, caption="Processed Image for Posture Analysis", use_column_width=True)

if __name__ == "__main__":
    main()
