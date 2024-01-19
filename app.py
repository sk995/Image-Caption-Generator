import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 200,
    }
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]
model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
def captionGenerate(image):
    image_parts = [
        {"mime_type":image.type,'data':image.read()}
    ]
    prompt_parts = [
      "Generate 3 Captions About This Image",
        image_parts[0]   
    ]    
    response = model.generate_content(prompt_parts)
    return response.text
      

def structure_app():
    st.set_page_config(page_title='Image Caption Generator Using GeminiPro',page_icon='🏝️')
    st.header('Image Caption Generator Using G:green[e]mini:blue[Pro] 🏝️')
    responses=''
    image=st.file_uploader(label='',type=['jpeg','jpg','png','webp'],accept_multiple_files=False,label_visibility='hidden')
    if image != None:
        st.image(image.read())
        if st.button('Generate Caption',use_container_width=True):
            with st.spinner('Loading...'):
                caption=captionGenerate(image=image)
                responses=caption

    with st.container(border=True):                    
        if responses != '':
	        st.write(responses.title())

if __name__ == "__main__":
    structure_app() 
