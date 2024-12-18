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

# Load intents from the JSON file
file_path = os.path.abspath("intents.json")
with open(file_path, "r") as file:
    intents = json.load(file)


# Create the vectorizer and classifier
vectorizer = TfidfVectorizer(ngram_range=(1, 4))
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

# training the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

def ChatBot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response
        
counter = 0

def main():
    global counter
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://th.bing.com/th/id/R.bf8f9e96e1bc35912e2f37327daaacad?rik=NX5ceQP1dFjHjQ&riu=http%3a%2f%2fbcrec.ac.in%2fpublic%2fstorage%2fslider_img%2fl7PmYgLFy46IHgSU6PXOabg7xSCKAjJOAdWGJj1P.jpg&ehk=q%2fER6nasbd9LxRr5k2lWGmEiOE2z8NL5ifNhcpu3WiQ%3d&risl=&pid=ImgRaw&r=0" alt="Banner" style="width: 100%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )
    # st.markdown(
    #         """
    #         <div style="display: flex; justify-content: center;">
    #             <img src="https://th.bing.com/th/id/OIP.DTyLgLWeuEQEm98Ga2OeVAHaHT?rs=1&pid=ImgDetMain" 
    #              alt="BCREC Logo" 
    #              style="width: 200px;">
    #          </div>
    #         """,
    #         unsafe_allow_html=True
    #         )
    st.markdown(
        '''
        <div style="display: flex; justify-content: center; align-items: center;">
            <h1 style="color: cyan; font-size: 36px; margin-right: 20px;">BCREC ChatBot</h1>
            <img src="https://th.bing.com/th/id/OIP.DTyLgLWeuEQEm98Ga2OeVAHaHT?rs=1&pid=ImgDetMain" 
            alt="BCREC Logo" 
            style="width: 50px;">
        </div>
        ''',
        unsafe_allow_html=True
    )
    # Add an image from a URL



    # Create a sidebar menu with options
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home Menu
    if choice == "Home":
        st.write("Welcome to the BCREC ChatBot. Please type a message and press Enter to start the conversation.")
       
        # Check if the chat_log.csv file exists, and if not, create it with column names
        if not os.path.exists('ChatBot\chat_log.csv'):
            with open('ChatBot\chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

        counter += 1
        user_input = st.text_input("You:", key=f"user_input_{counter}")

        if user_input:

            # Convert the user input to a string
            user_input_str = str(user_input)

            response = ChatBot(user_input)
            st.text_area("ChatBot:", value=response, height=120, max_chars=None, key=f"chatbot_response_{counter}")

            # Get the current timestamp
            timestamp = datetime.datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")

            # Save the user input and chatbot response to the chat_log.csv file
            with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input_str, response, timestamp])

            if response.lower() in ['goodbye', 'bye']:
                st.write("Thank you for chatting with me. Have a great day!")
                st.stop()

    # Conversation History Menu
    elif choice == "Conversation History":
        # Display the conversation history in a collapsible expander
        st.header("Conversation History")
        # with st.beta_expander("Click to see Conversation History"):
        with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                st.text(f"User: {row[0]}")
                st.text(f"ChatBot: {row[1]}")
                st.text(f"Timestamp: {row[2]}")
                st.markdown("---")

    elif choice == "About":
        st.write("The goal of this project is to develop a user-friendly chatbot for Dr. B.C. Roy Engineering College (BCREC) that can understand and respond to user inputs based on identified intents. Utilizing Natural Language Processing (NLP) techniques and a Logistic Regression model, the chatbot extracts intents and entities from user queries to provide accurate and relevant responses. Built with Streamlit, a Python library for creating interactive web applications, the chatbot ensures an engaging and seamless user experience, catering to the specific needs of BCREC students")

        st.subheader("Project Overview:")

        st.write("""
        The project is divided into two parts:
        1. NLP techniques and Logistic Regression algorithm is used to train the chatbot on labeled intents and entities.
        2. For building the Chatbot interface, Streamlit web framework is used to build a web-based chatbot interface. The interface allows users to input text and receive responses from the chatbot.
        """)

        st.subheader("Dataset:")

        st.write("""
        The dataset used in this project is a collection of labelled intents and entities. The data is stored in a list.
        - Intents: The intent of the user input 
        - Entities: The entities extracted from user input
        - Text: The user input text.
        """)

        st.subheader("Streamlit Chatbot Interface:")

        st.write("The chatbot interface is built using Streamlit. The interface includes a text input box for users to input their text and a chat window to display the chatbot's responses. The interface uses the trained model to generate responses to user input.")

        st.subheader("Conclusion:")

        st.write("In this project, a chatbot is built that can understand and respond to user input based on intents. The chatbot was trained using NLP and Logistic Regression and the interface was built using Streamlit. This project can be extended by adding more data, using more sophisticated NLP techniques, deep learning algorithms.")

if __name__ == '__main__':
    main()
