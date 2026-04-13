import streamlit as st
import requests

st.title("KP's Teacher Substitution App")

day = st.selectbox("Select the day for substitution:", ["Mo", "Tu", "We", "Th", "Fr"]) 
teachers_on_leave = st.text_input("Enter the names of teachers on leave (comma separated):")

if st.button("Generate Substitutions"):

    teacher_list = [t.strip() for t in teachers_on_leave.split(",") if t.strip()]

    response = requests.post("http://localhost:8000/generate_substitutions", json={
        "day": day,
        "teachers_on_leave": teacher_list
    })

    data = response.json()

    for item in data["substitutions"]:
        st.write(f"""
        📘 Class: {item['class']}
        📖 Subject: {item['subject']}
        ⏰ Period: {item['period']}
        👩‍🏫 Teacher: {item['assigned_teacher']}
        """)

