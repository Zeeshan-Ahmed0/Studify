import streamlit as st
import os
import time
from groq import Groq

st.markdown(
    """
    <style>
    /* General background and text styles */
    html, body, [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(to bottom right, 
    rgba(135, 206, 250, 0.8),  /* Light Sky Blue */
    rgba(255, 223, 186, 0.8),  /* Soft Peach */
    rgba(192, 192, 192, 0.8),  /* Bright Silver */
    rgba(169, 169, 169, 0.8),  /* Gray */
    rgba(240, 248, 255, 0.8),  /* Alice Blue */
    rgba(173, 216, 230, 0.8)   /* Light Blue */
);


        background-size: cover;
        font-family: 'Arial', sans-serif;
    }

    /* Header slide-right animation */
    @keyframes slide-right {
        0% {
            transform: translateX(-100%); /* Start off-screen to the left */
        }
        100% {
            transform: translateX(0); /* End at the normal position */
        }
    }

    /* Header slide-left animation */
    @keyframes slide-left {
        0% {
            transform: translateX(100%); /* Start off-screen to the right */
        }
        100% {
            transform: translateX(0); /* End at the normal position */
        }
    }

    /* Header slide-right animation for the title */
    .header-slide-right {
        display: inline-block;
        animation: slide-right 2s ease-out;
    }

    /* Subtitle slide-left animation */
    .header_description {
        display: inline-block;
        animation: slide-left 2s ease-out;
    }

    /* Button styles */
    .stButton button {
        background-color: #333333;
        color: white;
        border: 2px solid black;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }

    .stButton button:hover {
        background-color: #333;
    }
    .stSelectbox select {
        background-color: #333333;
        color: white;
        border: 2px solid black;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }

    .stSelectbox select:hover {
        background-color: #555555;
    }
    </style>
    """,
    unsafe_allow_html=True
)


client = Groq(api_key=("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"))
ss = st.session_state
session_vars = ["area", "subject", "subtopic", "level" , "tone", "language", "explanation", "mcqs", "answers", "feedback", "topic"]

for var in session_vars:
    ss.setdefault(var, None)

def get_response(prompt):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.2-90b-vision-preview",
    )
    return chat_completion.choices[0].message.content

def main_interface():
    st.markdown('<h1 class="header-slide-right">Studify</h1>', unsafe_allow_html=True)
    st.markdown('<h6 class="header_description">Learn the way you like!</h6>', unsafe_allow_html=True)
    time.sleep(2)

    if not ss.topic:
        area = st.radio(
            "Options:",("Select a Subject", "Search Manually"), horizontal = True)
        if area == "Select a Subject":
            st.write("Choose a subject from the list to explore specific topics and exercises.")
        elif area == "Search Manually":
            st.write("Use the search bar to manually find specific content or topics.")
        
        ss.area = area
                    
        if ss.area == "Search Manually":
            topic = st.text_input("Type any kind of subject or topic you want to learn about:")
            
        elif ss.area == "Select a Subject":
            topics = {
            "English": {
                "Grammar": ["Grammar", "Tenses", "Parts of Speech", "Sentence Structure", "Active Passive Voice", "Direct Indirect"],
                "Vocabulary": ["Vocabulary", "Synonyms", "Antonyms", "Prefixes/ Suffixes", "Homophones"],
                "Reading Comprehension": ["Reading Comprehension", "Essay Reading", "Story Reading", "New Article Reading"],
                "Essay Writing": ["Essay Writing", "Introduction", "Body Paragraphs", "Conclusion"],
                "Literature Analysis": ["Literature Analysis", "Poetry", "Non-fiction", "Novels", "Dramas"],
                "Creative Writing": ["Creative Writing", "Story Writing", "Dialogue Writing", "Script Writing"],
                "Speaking": ["Speaking", "Conversational", "Interviews", "Debate", "Public Speaking"],
                "Poetry Analysis": ["Poetry Analysis", "Rhythm", "Meter", "Imagery"]
            },
            "Maths": {
                "Word Problems": ["Word Problems", "Distance-Speed-Time", "Age Problems", "Work and Time", "Probability Problems"],
                "Algebra": ["Algebra", "Linear Equations", "Quadratic Equations", "Polynomials", "Exponents", "Factoring"],
                "Geometry": ["Geometry", "Lines and Angles", "Triangles", "Circles", "Surface Area and Volume", "Coordinate Geometry"],
                "Trigonometry": ["Trigonometry", "Trigonometric Ratios", "Sine, Cosine, Tangent", "Trigonometric Identities", "Height and Distance"],
                "Fractions": ["Fractions", "Simplifying Fractions", "Adding/Subtracting Fractions", "Multiplying/Dividing Fractions", "Mixed Numbers"],
                "Percentages": ["Percentages", "Percentage Increase/Decrease", "Discounts", "Profit and Loss", "Interest Calculation"],
                "Arithmetic Operations": ["Arithmetic Operations", "Addition", "Subtraction", "Multiplication", "Division", "Order of Operations (BODMAS)"]
            },
            "Science": {
                "Human Body Systems": ["Human Body Systems", "Circulatory System", "Respiratory System", "Nervous System", "Muscular System", "Digestive System"],
                "Atomic structure": ["Atomic structure", "Atoms", "Protons, Neutrons, Electrons", "Electron Configurations", "Periodic Table"],
                "Ecosystems": ["Ecosystems", "Food Chains", "Energy Flow", "Ecological Pyramids", "Biomes", "Environmental Factors"],
                "Forces and Motion": ["Forces and Motion", "Newton's Laws", "Friction", "Work and Energy", "Acceleration"],
                "States of Matter": ["States of Matter", "Solids", "Liquids", "Gases", "Plasma", "Changes in State"],
                "Energy and Work": ["Energy and Work", "Kinetic Energy", "Potential Energy", "Work-Energy Theorem", "Power"],
                "Plants": ["Plants", "Photosynthesis", "Plant Reproduction", "Plant Anatomy", "Types of Plants"],
                "Solar System": ["Solar System", "Planets", "Moons", "Asteroids", "Comets", "The Sun"]
            },
            "Social Studies": {
                "International Organizations": ["International Organizations", "United Nations", "World Health Organization", "World Bank", "International Monetary Fund"],
                "Climate Change": ["Climate Change", "Global Warming", "Carbon Footprint", "Effects of Climate Change", "Mitigation Strategies"],
                "Government and Democracy": ["Government and Democracy", "Types of Governments", "Democratic Systems", "Elections", "Political Rights"],
                "Human Rights and Responsibilities": ["Human Rights and Responsibilities", "Rights of Citizens", "International Human Rights", "Social Justice"],
                "Population Studies": ["Population Studies", "Population Growth", "Demographic Transition", "Urbanization", "Migration"],
                "World Cultures": ["World Cultures", "Cultural Diversity", "Globalization", "Cultural Identity", "Traditions and Customs"],
                "Religions": ["Religions", "Christianity", "Islam", "Hinduism", "Buddhism", "Judaism"],
                "Globalization and Trade": ["Globalization and Trade", "International Trade", "Economic Interdependence", "Trade Agreements", "Global Markets"]
            },
            "History": {
                "Islamic History": ["Islamic History", "The Origin of Humanity", "Early Islamic Civilization", "Golden Age of Islam", "Islamic Empires"],
                "Sub-Continent History": ["Sub-Continent History", "Ancient India", "Mughal Empire", "British India", "Partition of India"],
                "European History": ["European History", "Ancient Greece", "Roman Empire", "Middle Ages", "World Wars"],
                "American History": ["American History", "Colonial America", "American Revolution", "Civil War", "Modern America"],
                "Ancient Civilizations": ["Ancient Civilizations", "Mesopotamia", "Ancient Egypt", "Indus Valley Civilization", "Ancient China"],
                "Turkish (Ottoman) History": ["Turkish History", "Ottoman Empire", "Suleiman the Magnificent", "Decline of the Ottoman Empire"],
                "World Wars": ["World Wars", "World War I", "World War II", "Causes of War", "Aftermath and Consequences"]
            },
            "Islamiat": {
                "Life of Prophet Muhammad (PBUH)": ["Life of Prophet Muhammad (PBUH)", "Birth and Early Life", "Prophethood", "Migration to Medina", "The Farewell Sermon"],
                "Five Pillars of Islam": ["Five Pillars of Islam", "Shahada", "Salah", "Zakat", "Sawm", "Hajj"],
                "The Quran": ["The Quran", "Revelation", "Surahs", "Ayahs", "Exegesis of the Quran"],
                "Hadith": ["Hadith", "Types of Hadith", "Sahih Hadith", "Prophet's Sayings"],
                "Major Prophets": ["Major Prophets", "Prophet Adam (AS)", "Prophet Nuh (AS)" "Prophet Ibrahim (AS)", "Prophet Musa (AS)", "Prophet Isa (AS)", "Prophet Yusuf (AS)", "Prophet Muhammad (PBUH)"],
                "Shariah Law": ["Shariah Law", "Islamic Jurisprudence", "Rights and Duties", "Islamic Criminal Law"],
                "Jihad": ["Jihad", "Types of Jihad", "Jihad in Islam", "Jihad and Peace","The reality of Jihad"],
                "Islamic Ethics": ["Islamic Ethics", "Moral Teachings", "Rights of Others", "Social Justice in Islam"]
            },
            "Physics": {
                "Mechanics (Force, Motion)": ["Mechanics", "Newton's Laws", "Force", "Momentum", "Circular Motion"],
                "Electricity": ["Electricity", "Ohm's Law", "Circuits", "Electric Current", "Electromagnetic Fields"],
                "Magnetism": ["Magnetism", "Magnetic Fields", "Electromagnetic Induction", "Magnets", "Magnetic Force"],
                "Thermodynamics": ["Thermodynamics", "Laws of Thermodynamics", "Heat Transfer", "Entropy", "Internal Energy"],
                "Optics (Light and Mirrors)": ["Optics", "Reflection", "Refraction", "Lenses", "Optical Instruments"],
                "Waves and Sound": ["Waves and Sound", "Wave Properties", "Sound Waves", "Wave Interference", "Doppler Effect"],
                "Kinematics": ["Kinematics", "Velocity", "Acceleration", "Free Fall", "Projectile Motion"]
            },
            "Chemistry": {
                "Atomic Structure": ["Atomic Structure", "Atoms", "Protons, Neutrons, Electrons", "Electron Configuration", "Periodic Table"],
                "Periodic Table": ["Periodic Table", "Elements", "Groups and Periods", "Metals and Nonmetals", "Periodic Trends"],
                "Chemical Bonding": ["Chemical Bonding", "Ionic Bonds", "Covalent Bonds", "Metallic Bonds", "Molecular Geometry"],
                "Acids, Bases, and Salts": ["Acids, Bases, and Salts", "Properties of Acids and Bases", "Neutralization", "pH Scale"],
                "Chemical Reactions": ["Chemical Reactions", "Types of Reactions", "Balancing Equations", "Reaction Rates"],
                "Organic Chemistry": ["Organic Chemistry", "Hydrocarbons", "Alcohols", "Aldehydes and Ketones", "Polymerization"],
                "Biochiometry": ["Biochemistry", "Proteins", "Carbohydrates", "Lipids", "Nucleic Acids"],
                "Solutions and Mixtures": ["Solutions and Mixtures", "Solubility", "Concentration", "Types of Solutions"]
            },
            "Biology": {
                "Human Systems": ["Human Systems", "Circulatory System", "Digestive System", "Respiratory System", "Excretory System"],
                "Cell Structure and Function": ["Cell Structure and Function", "Prokaryotic Cells", "Eukaryotic Cells", "Cell Organelles", "Cell Membrane"],
                "Genetics and Heredity": ["Genetics", "DNA", "Gene Expression", "Inheritance", "Genetic Disorders"],
                "Human Anatomy and Physiology": ["Human Anatomy and Physiology", "Musculoskeletal System", "Nervous System", "Endocrine System"],
                "Plant Biology": ["Plant Biology", "Photosynthesis", "Plant Cells", "Plant Reproduction", "Plant Growth"],
                "Microorganisms": ["Microorganisms", "Bacteria", "Viruses", "Fungi", "Algae"],
                "Animal Kingdom": ["Animal Kingdom", "Vertebrates", "Invertebrates", "Mammals", "Amphibians"]
            },
            "Computer Studies": {
                "Programming Languages": ["Programming Languages", "Python", "Java", "C++", "JavaScript", "Ruby", "Swift"],
                "Programming Fundamentals": ["Programming Fundamentals", "Variables", "Loops", "Conditionals", "Functions"],
                "Algorithms and Data Structures": ["Algorithms", "Sorting", "Searching", "Arrays", "Linked Lists"],
                "Basics of Databases": ["Databases", "SQL", "Relational Databases", "Normalization", "Database Management"],
                "Computer Hardware and Software": ["Computer Hardware", "CPU", "RAM", "Motherboard", "Operating Systems"],
                "Networking Basics": ["Networking Basics", "IP Addressing", "Subnetting", "Routing", "Switching"],
                "Cybersecurity Essentials": ["Cybersecurity", "Encryption", "Firewall", "Malware", "Ethical Hacking"],
                "Artificial Intelligence Basics": ["AI Basics", "Machine Learning", "Neural Networks", "Natural Language Processing", "Computer Vision"],
                "Operating Systems": ["Operating Systems", "Linux", "Windows", "MacOS", "File Systems", "Process Management"]
            }
        }

            subject = st.selectbox("Choose a subject:", list(topics.keys()))
            topic = st.radio(f"Choose a topic for {subject}:", list(topics[subject].keys()))
            subtopic = st.selectbox(f"Choose a subtopic for {topic}:", topics[subject][topic])

        if ss.area:
            level = st.radio("Please select your proficiency level in the selected topic:", ("Beginner", "Intermediate", "Advanced"), horizontal=True)
            
            if st.button("Continue"):
                if ss.area == "Select a Subject":
                    ss.subject = subject
                    ss.subtopic = subtopic
                ss.level = level
                ss.topic = topic
                st.rerun()

    if ss.topic:
        if st.button("⬅️ Go Back", key="back", help="Go back"):
            for var in session_vars:
                if var != "area":
                    setattr(ss, var, None)
            st.rerun()

        tone = st.radio("Kindly select the way you want to learn the selected topic:",("Simple and easy", "Interesting and Engaging", "Detailed", "Storytelling"),horizontal = True)
        
        language = st.radio("Kindly select the Language you want to learn the selected topic:",("English", "Roman Urdu", "Hindi", "Urdu"),horizontal = True)
                    
        if st.button("Let's Learn"):
            ss.tone = tone
            ss.language = language
            ss.explanation = None
            ss.answers = None
            ss.feedback = None
            ss.mcqs = None
            
    if ss.tone:
        if ss.area == "Select a Subject":
            explanation_prompt = f"Provide an explanation on '{ss.subtopic}' related to '{ss.topic}', in a '{ss.tone}' tone, suitable for a '{ss.level}' level learner, strictly in '{ss.language}'. Avoid introductory phrases."
        elif ss.area == "Search Manually":
            explanation_prompt = f"Explain the topic {ss.topic}' in a '{ss.tone}' manner at the '{ss.level} level strictly in '{ss.language}'.\nDon't add any intro"
        
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
                    feedback_prompt = f"Evaluate and provide concise feedback in simple words on the following answers to the questions related to '{ss.topic}.'\nThe explanation used to explain the topic is: '{ss.explanation}.'\nThe mcqs are: '{ss.mcqs}.'\nThe answers given by me are: '{ss.answers}.'\nSpecify how many ansers are correct strictly accurately, if the answers are none or irrelevant say something like: 'Kindly give the answers correctly', and if there are some answers missing then specify which ones and request that they be done."
                    ss.feedback = get_response(feedback_prompt)
                    st.subheader("Feedback")
                    st.write(ss.feedback)
                
                
main_interface()
