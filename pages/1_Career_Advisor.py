import streamlit as st
import openai
from dotenv import load_dotenv  

client = openai.AzureOpenAI(
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
    api_key=st.secrets["AZURE_OPENAI_KEY"],
    api_version=st.secrets["AZURE_API_VERSION"],
)

DEPLOYMENT_NAME = st.secrets["AZURE_DEPLOYMENT_NAME"]

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
