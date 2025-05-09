import streamlit as st
import yaml
import os
from pathlib import Path

st.set_page_config(page_title="Fact-Checking CMS", page_icon="📝")
st.title("📝 Fact-Checking CMS")
st.markdown("Manage war-related facts for the fact-checking chatbot.")

DATA_PATH = "backend/data/war_data.yaml"

def load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, 'r') as f:
        return yaml.safe_load(f) or []

def save_data(data):
    with open(DATA_PATH, 'w') as f:
        yaml.dump(data, f)

# Load existing facts
facts = load_data()

# Add new fact
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

# Edit/Delete facts
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