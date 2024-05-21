import streamlit as st
from langchain_community import llms  
from langchain_community.llms import OpenAI


st.title('App PPS')

# Get OpenAI API key from the user
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

# Initialize session state for storing history
if 'history' not in st.session_state:
    st.session_state.history = []

def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    response = llm(input_text)
    st.info(response)
    # Save to history
    st.session_state.history.append({"prompt": input_text, "response": response})

# Form for user input
with st.form('my_form'):
    text = st.text_area('Enter text:', 'Enter text')
    submitted = st.form_submit_button('Submit')
    
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)

# Display question history
if st.session_state.history:
    st.write("## Question History")
    for i, entry in enumerate(st.session_state.history, 1):
        st.write(f"### Q{i}: {entry['prompt']}")
        st.write(f"A{i}: {entry['response']}")
