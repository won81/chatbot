import json
import requests
import streamlit as st
from streamlit_chat import message

st.header('Hugging Face Chatbot')
st.write("check out this [link](https://wide-shallow.tistory.com/entry/Streamlit%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-Chatbot-%EB%A7%8C%EB%93%A4%EA%B8%B0)")

if 'generated_responses' not in st.session_state:
    st.session_state['generated_responses'] = []

if 'user_inputs' not in st.session_state:
    st.session_state['user_inputs'] = []

if 'api_url' not in st.session_state:
    st.session_state['api_url'] = 'https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill'

if 'api_token' not in st.session_state:
    st.session_state['api_token'] = ''

st.session_state['api_url'] = st.text_input('API_URL: ', st.session_state['api_url'])
st.session_state['api_token'] = st.text_input('API_TOKEN: ', st.session_state['api_token'], type='password')

def query(payload):
    data = json.dumps(payload)
    response = requests.request('POST',
            st.session_state.api_url,
            headers = {'Authorization': f'Bearer {st.session_state.api_token}'},
            data = data)
    return json.loads(response.content.decode('utf-8'))

with st.form('form', clear_on_submit = True):
    user_input = st.text_input('Message: ', '')
    submitted = st.form_submit_button('Send')

if submitted and user_input:
    output = query({
        'inputs': {
            'past_user_inputs': st.session_state.user_inputs,
            'generated_responses': st.session_state.generated_responses,
            'text': user_input,
        },
    })

    st.session_state.user_inputs.append(user_input)
    st.session_state.generated_responses.append(output['generated_text'])

if st.session_state['generated_responses']:
    for i in range(0, len(st.session_state['generated_responses']), 1):
        message(st.session_state['user_inputs'][i], is_user = True, key=str(i) + '_user')
        message(st.session_state['generated_responses'][i], key=str(i))


