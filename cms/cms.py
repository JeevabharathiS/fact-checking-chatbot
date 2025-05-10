import streamlit as st
import yaml
import os
from pathlib import Path
import requests

st.set_page_config(page_title="Fact-Checking CMS", page_icon="📝")


def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.title("Login to Fact-Checking CMS")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if (
                username == st.secrets.auth.username
                and password == st.secrets.auth.password
            ):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.stop()

check_auth()

st.title("📝 Fact-Checking CMS")
st.markdown("Manage war-related facts for the fact-checking chatbot.")

# DATA_PATH = "backend/data/war_data.yaml"
DATA_PATH = "C:/Users/Jeevabharathi/What's Cookin/fact-checking-chatbot/backend/data/war_data.yaml"


def load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, 'r') as f:
        return yaml.safe_load(f) or []

def save_data(data):
    with open(DATA_PATH, 'w') as f:
        yaml.dump(data, f)
    try:
        response = requests.post("http://127.0.0.1:8000/reload-data")
        if response.status_code == 200:
            st.success("Data reloaded in chatbot.")
        else:
            st.warning("Failed to reload data in chatbot.")
    except Exception as e:
        st.warning(f"Error reloading data: {e}")


facts = load_data()


st.subheader("Add New Fact")
new_fact = st.text_area("Fact", placeholder="Enter the fact here...")
new_source = st.text_input("Source", placeholder="E.g., Government Press Release")
new_date = st.text_input("Date (YYYY-MM-DD)", placeholder="E.g., 2025-01-01")
if st.button("Add Fact"):
    if new_fact and new_source and new_date:
        facts.append({"fact": new_fact, "source": new_source, "date": new_date})
        save_data(facts)
        st.success("Fact added successfully!")
        st.rerun()
    else:
        st.error("Please fill in all fields.")


st.subheader("Manage Existing Facts")
for i, fact in enumerate(facts):
    with st.expander(f"Fact {i+1}: {fact['fact'][:50]}..."):
        edited_fact = st.text_area("Fact", value=fact['fact'], key=f"fact_{i}")
        edited_source = st.text_input("Source", value=fact['source'], key=f"source_{i}")
        edited_date = st.text_input("Date", value=fact['date'], key=f"date_{i}")
        if st.button("Update", key=f"update_{i}"):
            facts[i] = {"fact": edited_fact, "source": edited_source, "date": edited_date}
            save_data(facts)
            st.success("Fact updated successfully!")
            st.rerun()
        if st.button("Delete", key=f"delete_{i}"):
            facts.pop(i)
            save_data(facts)
            st.success("Fact deleted successfully!")
            st.rerun()