import streamlit as st

from ibm_watsonx_ai.foundation_models import ModelInference

#Set your credentials
API_KEY = "your api key here"
PROJECT_ID = "your project id here"
MODEL_ID = "ibm/granite-3-3-8b-instruct"
WATSONX_URL = "your watsonx url here"

# Define credentials dictionary
credentials = {
    "apikey": API_KEY,
    "url": WATSONX_URL
}

# Initialize Watsonx model
model = ModelInference(
    model_id=MODEL_ID,
    credentials=credentials,
    project_id=PROJECT_ID
)

# Define generation function
def generate_code(description, language):
    prompt = f"Generate a {language} code for an app with the following description:\n{description}"
    parameters = {
        "max_new_tokens": 800,
        "temperature": 0.7,
        "repetition_penalty": 1.1,
    }
    response = model.generate(prompt=prompt, params=parameters)
    return response['results'][0]['generated_text']

# Streamlit UI
st.set_page_config(page_title="Watsonx AI Code Generator", layout="centered")

st.title("💡 AI-Powered App Code Generator")
st.write("Generate app source code using IBM Watsonx LLM.")

# Input fields
description = st.text_area("📝 Enter your app description:", height=150)
language = st.selectbox("💻 Choose the programming language:", ["Python", "JavaScript", "HTML", "Java", "C++", "Other"])

# Generate button
if st.button("🚀 Generate Code"):
    if description.strip():
        with st.spinner("Generating code... please wait."):
            try:
                code = generate_code(description, language)
                st.success("✅ Code generated successfully!")
                st.code(code, language=language.lower())
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid app description.")
