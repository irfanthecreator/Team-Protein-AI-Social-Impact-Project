import streamlit as st
from PIL import Image

def main():
    st.title('Display Two Images')

    col1, col2 = st.columns(2)

    # Displaying first image in the first column
    with col1:
        st.header('First Image')
        image1 = Image.open('t1.jpg')
        st.image(image1, use_column_width=True)

    # Displaying second image in the second column
    with col2:
        st.header('Second Image')
        image2 = Image.open('t2.jpg')
        st.image(image2, use_column_width=True)

if __name__ == '__main__':
    main()
