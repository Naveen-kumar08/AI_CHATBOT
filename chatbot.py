import streamlit as st
from groq import Groq


def ask_groq(messages, model="llama-3.3-70b-versatile"):

    try:

        client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )


        response = client.chat.completions.create(

            model=model,

            messages=messages,

            temperature=0.7,

            max_tokens=4096
        )


        return response.choices[0].message.content


    except Exception as e:

        return f"❌ Error: {str(e)}"