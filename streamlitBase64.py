import streamlit as st
import base64
from io import BytesIO
from PIL import Image

# CSS for light-themed background with colors and layout
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #b3e5fc, #ffccbc, #b2dfdb, #f8bbd0);
        background-size: 400% 400%;
        animation: gradientAnimation 15s ease infinite;
        font-family: Arial, sans-serif;
    }

    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    h1, h2, h3 {
        font-size: 1.8rem !important;
        color: #444444 !important;
    }

    .stTextArea, .stButton, .stFileUploader {
        font-size: 1.2rem !important;
    }

    .stTextArea textarea, .stButton button, .stFileUploader input {
        border-radius: 8px;
        font-family: Arial, sans-serif;
    }

    .stButton button {
        background-color: #4fc3f7 !important;
        color: #ffffff !important;
        font-size: 1.2rem;
        border-radius: 8px;
    }
    .stButton button:hover {
        background-color: #039be5 !important;
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f0f0;
        color: #444444;
        text-align: center;
        padding: 10px;
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Logo and Title
st.image("codeproactiveLogo.jpg", width=200)  # Adjust the logo filename and size as needed
st.title("🌈 Base64 Converter EasyTool")

# Tabs for different conversion types
tab1, tab2 = st.tabs(["Decode Base64 to Content", "Encode Content to Base64"])

# Function to decode base64 to content
def decode_base64(input_data):
    try:
        decoded_data = base64.b64decode(input_data)
        return decoded_data
    except Exception as e:
        st.error("Error decoding Base64: " + str(e))
        return None

# Function to encode content to base64
def encode_base64(content):
    encoded_data = base64.b64encode(content).decode('utf-8')
    return encoded_data

# Tab 1: Decode Base64 to respective content
with tab1:
    st.header("Decode Base64")
    base64_input = st.text_area("Paste Base64 data here:")
    decode_button = st.button("Decode")

    if decode_button and base64_input:
        decoded_data = decode_base64(base64_input)

        if decoded_data:
            if decoded_data[:4] == b'%PDF':
                st.write("Detected PDF file.")
                st.download_button("Download PDF", data=decoded_data, file_name="output.pdf")
            elif decoded_data[:4] == b'\xff\xd8\xff\xe0':
                st.write("Detected Image file.")
                image = Image.open(BytesIO(decoded_data))
                st.image(image, caption="Decoded Image", use_column_width=True)
                st.download_button("Download Image", data=decoded_data, file_name="output.jpg")
            else:
                st.write("Detected Text data.")
                decoded_text = decoded_data.decode('utf-8')
                st.text_area("Decoded Text:", decoded_text, height=200)
                st.download_button("Download Text", data=decoded_text, file_name="output.txt")

# Tab 2: Encode Content to Base64
with tab2:
    st.header("Encode Content to Base64")
    
    uploaded_file = st.file_uploader("Upload a file to convert to Base64", type=["txt", "jpg", "png", "pdf"])
    text_input = st.text_area("Or paste text here to encode:", disabled=bool(uploaded_file))
    
    if uploaded_file:
        st.warning("File attached. Remove it to use the text input option.")

    encode_button = st.button("Convert")

    if encode_button:
        if uploaded_file is not None:
            file_data = uploaded_file.read()
            encoded_data = encode_base64(file_data)
            st.text_area("Encoded Base64:", encoded_data, height=200)
            st.download_button("Download Base64 as .txt", data=encoded_data, file_name="encoded.txt")
        
        elif text_input:
            encoded_data = encode_base64(text_input.encode('utf-8'))
            st.text_area("Encoded Base64:", encoded_data, height=200)
            st.download_button("Download Base64 as .txt", data=encoded_data, file_name="encoded.txt")

st.info("Note: For images and PDFs, a preview will be displayed when possible. For other file types, content will be shown as text.")

# Footer with copyright notice
st.markdown(
    "<div class='footer'>"
    "Copyright © 2024 | Design & Developed by CodeProactive"
    "</div>",
    unsafe_allow_html=True
)
