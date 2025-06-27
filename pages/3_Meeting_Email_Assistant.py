import streamlit as st
import os
import openai
from dotenv import load_dotenv  
from openai import AzureOpenAI

client = openai.AzureOpenAI(
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
    api_key=st.secrets["AZURE_OPENAI_KEY"],
    api_version=st.secrets["AZURE_API_VERSION"],
)

DEPLOYMENT_NAME = st.secrets["AZURE_DEPLOYMENT_NAME"]

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
