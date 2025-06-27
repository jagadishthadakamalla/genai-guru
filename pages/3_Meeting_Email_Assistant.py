import streamlit as st
import os
from dotenv import load_dotenv  
from openai import AzureOpenAI

load_dotenv()
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2025-01-01-preview",
)

DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")

st.title("📅 Meeting & Email Assistant")
st.markdown("Summarize meeting notes or generate a professional email draft.")

note = st.text_area("Paste your meeting notes or email content")
option = st.radio("Choose output:", ["Summarize Notes", "Generate Email"])
generate_output = st.button("✍️ Generate Output")
if generate_output and note:
    with st.spinner("Generating..."):
        prompt = (
            "Summarize this meeting:" if option == "Summarize Notes"
            else "Write a professional email based on this content:"
        )

        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that generates summaries and writes professional emails."
                },
                {
                    "role": "user",
                    "content": f"{prompt}\n{note}"
                }
            ],
            temperature=0.6,
            max_tokens=500
        )
        result = response.choices[0].message.content
    st.success("Here’s the output:")
    st.write(result)