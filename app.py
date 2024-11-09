import streamlit as st
import os
from groq import Groq

client = Groq(api_key=("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"))

ss = st.session_state

session_vars = ["level", "subject", "topic", "tone", "topics", "explanation", "mcqs", "answer", "answers", "feedback"]
for var in session_vars:
    ss.setdefault(var, None)

def get_response(prompt):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

st.set_page_config(page_title="Studify", layout="centered")
def main_interface():
    st.title("Studify")
    st.markdown("###### Study the way you want")
    subject = st.sidebar.radio(
        "Choose a subject",
        ("English", "Mathematics", "Science", "Social Studies", "History", "Geography", "Physics", "Chemistry", "Biology", "Computer Science"))

    if st.sidebar.button("Proceed"):
        ss.subject = subject
    if ss.subject:
        st.header(f"Please select your proficiency level in {ss.subject}")
        level = st.radio("Select Level", ("Beginner", "Intermediate", "Advanced"), horizontal=True)
        
        if st.button("Continue"):
            ss.level = level
        if ss.level:
            topic_prompt = f"Generate 8 topics related to {ss.subject} for {ss.level} level without any description."
            ss.topics = get_response(topic_prompt)

            st.subheader("What do you want to learn about:")
            st.write(ss.topics)

            topic_selection = st.text_input("Enter the topic you want to learn about:")

            tone = st.radio("Kindly select the way you want to learn the selected topic",
                ("Simple and easy", "Humorous and Fun", "Interesting and Engaging", "Detailed and In-Depth", "Storytelling manner"))

            if st.button("Let's Learn"):
                ss.topic= topic_selection
                ss.tone = tone
            if ss.topic:
                explanation_prompt = f"Explain the topic '{ss.topic}' briefly in a {ss.tone} manner related to {ss.subject} for {ss.level} level. If there isn't any topic specified say 'Kindly enter a topic from the given list'."
                ss.explanation = get_response(explanation_prompt)
                st.subheader(f"Explanation on {ss.topic}")
                st.write(ss.explanation)
                
                if ss.explanation:
                    if st.button("Take a test"):
                        mcq_prompt = f"Generate 5 strictly 'SHORT' multiple-choice questions related to the topic '{ss.topic}', using the explanation {ss.explanation} at a {ss.level} level.\nPlease ensure each answer option is on a new line, and do not specify the correct answers."
                        ss.mcqs = get_response(mcq_prompt)
                    if ss.mcqs:
                        st.subheader("Test: Answer the following questions")
                        st.write(ss.mcqs)
                        ss.answer = st.text_area("Write your answers here:")
                    if st.button("Submit Answers"):
                        ss.answers = ss.answer
                        feedback_prompt = f"Evaluate and provide concise feedback in simple words on the following answers to the questions related to '{ss.topic}.'\nthe explanation used to explain the topic is: '{ss.explanation}.'\nThe mcqs are: '{ss.mcqs}.'\nThe answers given by me are: '{ss.answers}.'\nSpecify how many ansers are correct, if the answers are none or irrelevant say something like: 'Kindly give the answers correctly', and if there are some answers missing then specify which ones and request that they be done."
                        ss.feedback = get_response(feedback_prompt)
                        st.subheader("Feedback")
                        st.write(ss.feedback)   
main_interface()
