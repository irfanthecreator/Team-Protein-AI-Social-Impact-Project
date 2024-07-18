import streamlit as st
import playsound

# Streamlit 제목
st.title("버튼을 누르면 소리가 나는 애플리케이션")

# 사운드 파일 읽기
sound_file = "audio/beep.mp3"  # 사운드 파일 경로를 설정하세요

# 버튼 생성
if st.button("소리 재생"):
    playsound.playsound(sound_file)
    st.write("소리가 재생되었습니다!")

