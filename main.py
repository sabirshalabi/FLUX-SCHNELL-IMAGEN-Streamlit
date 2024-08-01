import streamlit as st
import replicate
import os
from dotenv import load_dotenv
import logging
import base64
from io import BytesIO
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

def verify_api_key(api_key):
    os.environ["REPLICATE_API_TOKEN"] = api_key
    try:
        replicate.Client(api_token=api_key).models.get("black-forest-labs/flux-schnell")
        return True
    except Exception:
        return False

def generate_image(prompt, aspect_ratio, output_format, output_quality, api_key):
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    try:
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "output_format": output_format,
                "output_quality": output_quality
            }
        )
        return output[0] if isinstance(output, list) else output
    except Exception as e:
        logging.error(f"Image generation failed: {str(e)}")
        raise Exception(f"Image generation failed: {str(e)}")

def get_image_download_link(img_url, filename, text):
    response = requests.get(img_url)
    img = BytesIO(response.content)
    b64 = base64.b64encode(img.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Streamlit app
st.set_page_config(layout="wide", page_title="Flux Schnell Image Generator")

# Sidebar for API key input and verification
with st.sidebar:
    st.title("API Key Configuration")
    api_key = st.text_input("Enter your Replicate API key:", type="password")
    if st.button("Verify API Key"):
        if verify_api_key(api_key):
            st.success("API key verified successfully!")
            st.session_state.verified_api_key = api_key
        else:
            st.error("Invalid API key. Please try again.")
            st.session_state.verified_api_key = None

# Main app
st.title("Flux Schnell Image Generator")
st.write("Generate amazing images using the Flux Schnell model")

# Input column
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Input")
    prompt = st.text_area("Enter your prompt:", height=100, help="Describe the image you want to generate")
    
    aspect_ratio = st.selectbox(
        "Select aspect ratio:",
        ["1:1", "16:9", "9:16"],
        format_func=lambda x: f"{x} {'□' if x == '1:1' else '▭' if x == '16:9' else '▯'}",
        help="Choose the aspect ratio for your generated image"
    )
    
    with st.expander("Advanced Options"):
        output_format = st.selectbox("Select output format:", ["webp", "png"], help="Choose the file format for your generated image")
        output_quality = st.slider("Select output quality:", 1, 100, 90, help="Set the quality of the output image (higher values mean better quality but larger file size)")

    if st.button("Generate Image"):
        if not prompt:
            st.error("Please enter a prompt.")
        elif not hasattr(st.session_state, 'verified_api_key') or not st.session_state.verified_api_key:
            st.error("Please verify your API key in the sidebar before generating an image.")
        else:
            try:
                with st.spinner("Generating image..."):
                    image_url = generate_image(prompt, aspect_ratio, output_format, output_quality, st.session_state.verified_api_key)
                st.session_state.current_image = image_url
                st.session_state.history.append({"prompt": prompt, "image_url": image_url})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logging.error(f"Error details: {str(e)}")

# Output column
with col2:
    st.subheader("Output")
    if hasattr(st.session_state, 'current_image'):
        st.image(st.session_state.current_image, caption="Generated Image", use_column_width=True)
        st.download_button("Download Image", get_image_download_link(st.session_state.current_image, "generated_image.png", "Download Image"), file_name="generated_image.png", mime="image/png")

# Image Gallery
if 'history' not in st.session_state:
    st.session_state.history = []

if st.session_state.history:
    st.subheader("Image Gallery")
    gallery_cols = st.columns(5)
    for i, item in enumerate(reversed(st.session_state.history[-5:])):
        with gallery_cols[i % 5]:
            st.image(item["image_url"], width=150)
            if st.button(f"Reuse Prompt {i+1}"):
                prompt = item["prompt"]
                st.experimental_rerun()
            if st.button(f"Expand Image {i+1}", key=f"expand_{i}"):
                st.session_state.expanded_image = item["image_url"]

# Expanded Image
if 'expanded_image' in st.session_state:
    st.subheader("Expanded Image")
    st.image(st.session_state.expanded_image, caption="Generated Image", use_column_width=True)
    st.download_button("Download Image", get_image_download_link(st.session_state.expanded_image, "generated_image.png", "Download Image"), file_name="generated_image.png", mime="image/png")

# Display API key status
if hasattr(st.session_state, 'verified_api_key') and st.session_state.verified_api_key:
    st.sidebar.success("API key is verified and ready to use.")
elif os.getenv("REPLICATE_API_TOKEN"):
    st.sidebar.info("Using API key from environment variable. You can override it in the sidebar.")
else:
    st.sidebar.warning("No verified API key. Please enter and verify your API key in the sidebar.")
