import streamlit as st
import openai
from dotenv import load_dotenv  

client = openai.AzureOpenAI(
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
    api_key=st.secrets["AZURE_OPENAI_KEY"],
    api_version=st.secrets["AZURE_API_VERSION"],
)

DEPLOYMENT_NAME = st.secrets["AZURE_DEPLOYMENT_NAME"]

st.title("📈 Personal Productivity Tracker")
st.markdown("Track your daily goal and get a motivational boost.")

task = st.text_input("What's one thing you want to accomplish today?")
done = st.checkbox("Did you complete it?")

if task:
    if done:
        st.success(f"✅ Great job completing: {task}")
    else:
        st.warning(f"⏳ Still pending: {task}")

if st.button("💡 Get Motivational Quote"):
    with st.spinner("Fetching inspiration..."):
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a motivational coach who shares short quotes to inspire productivity."
                },
                {
                    "role": "user",
                    "content": "Give me a motivational quote to stay productive."
                }
            ],
            temperature=0.8,
            max_tokens=80
        )
        quote = response.choices[0].message.content
    st.info(quote)
