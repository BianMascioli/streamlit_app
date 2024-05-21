import streamlit as st
from langchain_community import llms  
from langchain_community.llms import OpenAI
import streamlit as st
from langchain_community.llms import OpenAI

st.title('App PPS')

# Get OpenAI API key from the user
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

# Initialize session state for storing history and saved histories
if 'history' not in st.session_state:
    st.session_state.history = []

if 'saved_histories' not in st.session_state:
    st.session_state.saved_histories = {}

def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    response = llm(input_text)
    st.info(response)
    # Save to history
    st.session_state.history.append({"prompt": input_text, "response": response})

# Form for user input
with st.form('my_form'):
    text = st.text_area('Enter text:', 'Escriba su pregunta')
    submitted = st.form_submit_button('Enviar')
    
    if not openai_api_key.startswith('sk-'):
        st.warning('Por favor introduzca su OpenAI API key!', icon='⚠')
    
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)

# Section to save the current history
with st.form('save_form'):
    history_name = st.text_input('Escriba un nombre para guardar el historial:')
    save_history = st.form_submit_button('Guardar historial')
    
    if save_history:
        if history_name:
            st.session_state.saved_histories[history_name] = st.session_state.history.copy()
            st.session_state.history.clear()
            st.success(f'Historial guardado como "{history_name}"')
        else:
            st.warning('Por favor introduzca un nombre para el historial!', icon='⚠')

# Display question history
if st.session_state.history:
    st.write("## Historial Actual")
    for i, entry in enumerate(st.session_state.history, 1):
        st.write(f"### Q{i}: {entry['prompt']}")
        st.write(f"A{i}: {entry['response']}")

# Display saved histories
if st.session_state.saved_histories:
    st.write("## Historiales guardados")
    for name, history in st.session_state.saved_histories.items():
        st.write(f"### Historial: {name}")
        for i, entry in enumerate(history, 1):
            st.write(f"#### Q{i}: {entry['prompt']}")
            st.write(f"A{i}: {entry['response']}")
