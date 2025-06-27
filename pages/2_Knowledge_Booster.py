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

st.title("📚 Knowledge Booster")
st.markdown("Type a concept or tech topic you're curious about.")

concept = st.text_input("Enter a topic (e.g., 'What is RAG in GenAI?')")
get_explanation = st.button("📘 Get Explanation")
if get_explanation and concept:
    with st.spinner("Explaining..."):
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical educator who explains concepts simply with examples."
                },
                {
                    "role": "user",
                    "content": f"Explain this concept simply with an example:\n{concept}"
                }
            ],
            temperature=0.5,
            max_tokens=600
        )
        explanation = response.choices[0].message.content
    st.success("Explanation:")
    st.write(explanation)
