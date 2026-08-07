import os
import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
from dotenv import load_dotenv


load_dotenv()


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)