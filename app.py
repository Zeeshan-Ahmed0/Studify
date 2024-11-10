import streamlit as st
import os
from groq import Groq

client = Groq(api_key=("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"))

ss = st.session_state

session_vars = ["level", "subject", "tone", "explanation", "mcqs", "answers", "feedback", "topic"]
for var in session_vars:
    ss.setdefault(var, None)

def get_response(prompt):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.2-90b-vision-preview",
    )
    return chat_completion.choices[0].message.content

def main_interface():
    st.title("Studify")
    st.markdown("###### Study the way you want")
    subject = st.sidebar.radio(
        "Choose a subject",
        ("English", "Mathematics", "Science", "Social Studies", "History", "Islamiat", "Physics", "Chemistry", "Biology", "Computer Science"))

    if st.sidebar.button("Proceed"):
        for var in session_vars:
            setattr(ss, var, None)
        ss.subject = subject
            
    if ss.subject and not ss.topic:
        st.header(f"Kindly select the {ss.subject} topic you want to learn about:")
        
        if ss.subject == "English":
            topic = st.radio("Options:", ["Grammar", "Vocabulary", "Reading Comprehension", "Essay Writing", "Literature Analysis", "Creative Writing", "Speaking", "Poetry Analysis"], index=0)
        elif ss.subject == "Mathematics":
            topic = st.radio("Options:", ["Word Problems", "Algebra", "Geometry", "Trignometry", "Fractions", "Percentages" , "Arithmetic Operations"], index=0)
        elif ss.subject == "Science":
            topic = st.radio("Options:", ["Human Body Systems", "Atomic structure", "Ecosystems", "Forces and Motion", "States of Matter", "Energy and Work", "Plants", "Solar System"], index=0)
        elif ss.subject == "Social Studies":
            topic = st.radio("Options:", ["International Organizations","Climate Change","Government and Democracy", "Human Rights and Responsibilities", "Population Studies", "World Cultures", "Religions", "Globalization and Trade"], index=0)
        elif ss.subject == "History":
            topic = st.radio("Options:", ["Islamic History", "Sub-Continent History", "European History", "American History", "Ancient Civilizations", "Turkish (Ottoman) History", "World Wars"], index=0)
        elif ss.subject == "Islamiat":
            topic = st.radio("Options:", ["Life of Prophet Muhammad (PBUH)", "Five Pillars of Islam", "The Quran", "Hadith", "Major Prophets", "Shariah Law", "Jihad", "Islamic Ethics"], index=0)
        elif ss.subject == "Physics":
            topic = st.radio("Options:", ["Mechanics (Force, Motion)", "Electricity", "Magnetism", "Thermodynamics", "Optics (Light and Mirrors)", "Waves and Sound","Kinematics (Velocity, Acceleration)"], index=0)
        elif ss.subject == "Chemistry":
            topic = st.radio("Options:", ["Atomic Structure", "Periodic Table", "Chemical Bonding", "Acids, Bases, and Salts", "Chemical Reactions", "Organic Chemistry", "Biochiometry","Solutions and Mixtures"], index=0)
        elif ss.subject == "Biology":
            topic = st.radio("Options:", ["Human Systems", "Cell Structure and Function", "Genetics and Heredity", "Human Anatomy and Physiology", "Plant Biology", "Microorganisms", "Animal Kingdom"], index=0)
        elif ss.subject == "Computer Studies":
            topic = st.radio("Options:", ["Programming Languages", "Programming Fundamentals", "Algorithms and Data Structures", "Basics of Databases", "Computer Hardware and Software", "Networking Basics", "Cybersecurity Essentials", "Artificial Intelligence Basics", "Operating Systems"], index=0)
            
        
        st.header(f"Please select your proficiency level in {ss.subject}")
        level = st.radio("Select Level", ("Beginner", "Intermediate", "Advanced"), horizontal=True)
        
        tone = st.radio("Kindly select the way you want to learn the selected topic:",
            ("Simple and easy", "Humorous and Fun", "Interesting and Engaging", "Detailed", "Storytelling"))

        if st.button("Let's Learn"):
            ss.level = level
            ss.topic = topic
            ss.tone = tone
            st.rerun()
            
    if ss.topic:
        if st.button("⬅️ Back", key="back", help="Go back"):
            for var in session_vars:
                if var != "subject":
                    setattr(ss, var, None)
            st.rerun()
        
        explanation_prompt = f"Explain the topic '{ss.topic}' briefly in a '{ss.tone}' manner related to '{ss.subject}' at a '{ss.level}' level.\nDon't add any intro"
        ss.explanation = get_response(explanation_prompt)
        st.write(ss.explanation)
        
        if ss.explanation:
            if st.button("Take a test"):
                mcq_prompt = f"Generate 5 'SHORT' multiple-choice questions related to the topic '{ss.topic}', strictly at the '{ss.level}' level.\nThe explanation used to explain the topic is:\n '{ss.explanation}'.\nPlease ensure each answer option is on a new line, and do not specify the correct answers."
                ss.mcqs = get_response(mcq_prompt)
            if ss.mcqs:
                st.subheader("Test: Answer the following questions")
                st.write(ss.mcqs)
                answer = st.text_area("Write your answers here:", height=120, placeholder="Please attempt the answers like:\n1. A\n2. C\n3. B..." )
                if st.button("Submit Answers"):
                    ss.answers = answer
                    feedback_prompt = f"Evaluate and provide concise feedback in simple words on the following answers to the questions related to '{ss.topic}.'\nThe explanation used to explain the topic is: '{ss.explanation}.'\nThe mcqs are: '{ss.mcqs}.'\nThe answers given by me are: '{ss.answers}.'\nSpecify how many ansers are correct, if the answers are none or irrelevant say something like: 'Kindly give the answers correctly', and if there are some answers missing then specify which ones and request that they be done."
                    ss.feedback = get_response(feedback_prompt)
                    st.subheader("Feedback")
                    st.write(ss.feedback)   
                
main_interface()
