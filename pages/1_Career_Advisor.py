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

st.title("🧭 Career Advisor")
st.markdown("Ask your career-related question and get advice powered by GenAI.")

career_question = st.text_input("Enter your career question")
get_advice = st.button("💡 Get Advice")
if get_advice and career_question:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior career advisor for IT professionals."
                },
                {
                    "role": "user",
                    "content": career_question
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        answer = response.choices[0].message.content
    st.success("Here’s your personalized career advice:")
    st.write(answer)