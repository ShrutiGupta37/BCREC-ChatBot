import os
import json
import datetime
import csv
import nltk
import ssl
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Create a function to ensure the directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Load intents from the JSON file
file_path = os.path.join(os.getcwd(), "ChatBot University", "intents.json")
with open(file_path, "r", encoding='utf-8') as file:
    intents = json.load(file)

# Create the vectorizer and classifier
vectorizer = TfidfVectorizer(ngram_range=(1, 4))
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents.get('intents', []):
    if isinstance(intent, dict) and 'patterns' in intent and 'tag' in intent:
        for pattern in intent['patterns']:
            tags.append(intent['tag'])
            patterns.append(pattern)

# Train the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

# Chatbot function
def ChatBot(input_text):
    input_text = input_text.lower().strip()  # Clean input
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents.get('intents', []):
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response

# Ensure the directory for chat logs exists
ensure_directory_exists('ChatBot University')

counter = 0

def main():
    global counter
    st.markdown("""
        <div style="display: flex; justify-content: center;">
            <img src="https://static.vecteezy.com/system/resources/previews/023/480/009/original/breast-cancer-awareness-symbol-pink-ribbon-isolated-on-black-background-vector.jpg" 
            alt="Breast Cancer Awareness" 
            style="width: 200px;">
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<h1 style="color: pink; text-align: center; font-size: 36px;">Chatbot for Breast Cancer</h1>', unsafe_allow_html=True)

    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home Menu
    if choice == "Home":
        st.write("Welcome to the chatbot. Please type a message and press Enter to start the conversation.")
        
        # Check if the chat_log.csv file exists, and if not, create it with column names
        if not os.path.exists('ChatBot University/chat_log.csv'):
            with open('ChatBot University/chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

        counter += 1
        user_input = st.text_input("You:", key=f"user_input_{counter}")

        if user_input:
            user_input_str = str(user_input)
            response = ChatBot(user_input)
            st.text_area("ChatBot:", value=response, height=120, max_chars=None, key=f"chatbot_response_{counter}")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open('ChatBot University/chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input_str, response, timestamp])

            if response.lower() in ['goodbye', 'bye']:
                st.write("Thank you for chatting with me. Have a great day!")
                st.stop()

    # Conversation History Menu
    elif choice == "Conversation History":
        st.header("Conversation History")
        with open('ChatBot University/chat_log.csv', 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                st.text(f"User: {row[0]}")
                st.text(f"ChatBot: {row[1]}")
                st.text(f"Timestamp: {row[2]}")
                st.markdown("---")

    # About Menu
    elif choice == "About":
        st.write("The goal of this project is to create a chatbot that can understand and respond to user input based on intents.")
        st.subheader("Project Overview:")
        st.write("""
        The project uses NLP techniques, Logistic Regression, and Streamlit to create a chatbot interface.
        """)
        st.subheader("Dataset:")
        st.write("""
        The dataset contains labeled intents and entities used to train the chatbot.
        """)
        st.subheader("Conclusion:")
        st.write("The project builds a chatbot using NLP, Logistic Regression, and Streamlit.")

if __name__ == '__main__':
    main()
