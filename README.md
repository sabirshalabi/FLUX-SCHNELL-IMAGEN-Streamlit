# Flux Schnell Image Generator

This Streamlit app allows you to generate images using the Flux Schnell model from Replicate.

## Features

* **Image Generation:** Generate images based on your text prompts.
* **Image Gallery:** Browse through your recently generated images.
* **Image Expansion:** Click on an image in the gallery to view it in full screen.
* **Download Button:** Download the expanded image.
* **Prompt Reuse:** Reuse a previous prompt to generate a new image.

## Getting Started

1. **Install Dependencies:**
   ```bash
   pip install streamlit replicate dotenv
   ```

2. **Create a Replicate API Key:**
   * Sign up for a Replicate account at [https://replicate.com/](https://replicate.com/).
   * Create a new API key in your Replicate account settings.

3. **Set Up Environment Variables:**
   * Create a `.env` file in the same directory as your Streamlit app.
   * Add the following line to the `.env` file, replacing `YOUR_REPLICATE_API_KEY` with your actual API key:
     ```
     REPLICATE_API_TOKEN=YOUR_REPLICATE_API_KEY
     ```

4. **Run the App:**
   ```bash
   streamlit run main.py
   ```

## Usage

1. **Enter your Replicate API key:** In the sidebar, enter your Replicate API key and click "Verify API Key".
2. **Enter your prompt:** In the "Input" section, enter a text prompt describing the image you want to generate.
3. **Choose options:** Select the aspect ratio, output format, and output quality.
4. **Generate the image:** Click "Generate Image".
5. **Browse the gallery:** View your generated images in the "Image Gallery".
6. **Expand an image:** Click on an image in the gallery to view it in full screen.
7. **Download the image:** Click the "Download Image" button in the expanded view.
8. **Reuse a prompt:** Click the "Reuse Prompt" button next to an image in the gallery to generate a new image using the same prompt.

## Notes

* The app uses the `replicate` library to interact with the Replicate API.
* The app uses Streamlit's session state to store generated images and prompts.
* The app uses CSS to style the UI and center the expanded image.

## License

This project is licensed under the MIT License.