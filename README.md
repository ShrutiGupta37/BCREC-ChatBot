# BCREC-ChatBot
## Overview
The BCREC ChatBot is a chatbot designed for Dr. B.C. Roy Engineering College. It uses Natural Language Processing (NLP) to understand user inputs and provide responses. The chatbot recognizes different types of questions or requests (called "intents") and responds with pre-defined answers.
## Features
- Simple and interactive interface built with Streamlit for easy communication
- Identifies the type of query based on user input
- Provides relevant responses based on matched patterns and user intent
- Saves and displays previous interactions with the chatbot
- Records user input, chatbot response, and timestamps for tracking conversations
## Technologies Used
- Python
- NLTK
- Scikit-learn
- Streamlit
- JSON for intents data
## Installation
1. Clone the repo
   ```bash
   git clone https://github.com/ShrutiGupta37/BCREC-ChatBot.git
2. Install Required Packages
   ```bash
   pip install -r requirements.txt
3. Download NLTK Data
   ```bash
   import nltk
   nltk.download('punkt')
## Usage
* To run the chatbot application, execute the following command:
   ```bash
   tstreamlit run app.py
## Intents Data
The chatbot's behavior is defined by the intents.json file, which contains various tags, patterns, and responses. You can modify this file to add new intents or change existing ones.
## Conversation History
The chatbot saves the conversation history in a CSV file (chat_log.csv). You can view past interactions by selecting the "Conversation History" option in the sidebar.
## Acknowledgments
- NLTK for natural language processing.
- Scikit-learn for machine learning algorithms.
- Streamlit for building the web interface.
  

  

