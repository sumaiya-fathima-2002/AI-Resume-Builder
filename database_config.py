import pymysql
import streamlit as st
from transformers import pipeline
from googletrans import Translator

# --- DB CONNECTION ---
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Admin12@', # UPDATE THIS
        db='skillsmart_db',
        cursorclass=pymysql.cursors.DictCursor
    )

# --- SHARED AI MODELS ---
@st.cache_resource
def load_shared_engines():
    # Zero-Shot Classifier for Domain, Tier, and Skills
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    translator = Translator()
    return classifier, translator