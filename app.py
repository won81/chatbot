import json
import requests
import streamlit as st
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard
from streamlit_chat import message

st.header('Chatbot')

HuggingFaceTab, GoogleBardTab = st.tabs(["blenderbot-400M-distill", "Google Bard"])

with HuggingFaceTab:
    if 'generated_responses' not in st.session_state:
        st.session_state['generated_responses'] = []

    if 'user_inputs' not in st.session_state:
        st.session_state['user_inputs'] = []

    if 'api_url' not in st.session_state:
        st.session_state['api_url'] = ''

    if 'api_token' not in st.session_state:
        st.session_state['api_token'] = ''

    st.session_state['api_url'] = st.text_input('API_URL: ', st.session_state['api_url'])
    st.session_state['api_token'] = st.text_input('API_TOKEN: ', st.session_state['api_token'], type='password')

    def query_to_huggingface(payload):
        data = json.dumps(payload)
        response = requests.request('POST',
                st.session_state.api_url,
                headers = {'Authorization': f'Bearer {st.session_state.api_token}'},
                data = data)
        return json.loads(response.content.decode('utf-8'))

    with st.form('form_for_huggingface', clear_on_submit = True):
        user_input = st.text_input('Message: ', '')
        submitted = st.form_submit_button('Send')

    if submitted and user_input:
        output = query_to_huggingface({
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
            message(st.session_state['user_inputs'][i], is_user = True, key=str(i) + '_huggineface_user')
            message(st.session_state['generated_responses'][i], key=str(i) + '_huggingface')

with GoogleBardTab:
    if 'generated_responses' not in st.session_state:
        st.session_state['generated_responses'] = []

    if 'user_inputs' not in st.session_state:
        st.session_state['user_inputs'] = []

    if 'token' not in st.session_state:
        st.session_state['token'] = ''

    if 'psidts' not in st.session_state:
        st.session_state['psidts'] = ''

    if 'psidcc' not in st.session_state:
        st.session_state['psidcc'] = ''

    st.session_state['token'] = st.text_input('TOKEN: ', st.session_state['token'], type='password')
    st.session_state['psidts'] = st.text_input('1PSIDTS: ', st.session_state['psidts'], type='password')
    st.session_state['psidcc'] = st.text_input('1PSIDCC: ', st.session_state['psidcc'], type='password')


    session = requests.Session()
    session.headers = SESSION_HEADERS
    session.cookies.set("__Secure-1PSID", st.session_state.token)
    session.cookies.set("__Secure-1PSIDTS", st.session_state.psidts)
    session.cookies.set("__Secure-1PSIDCC", st.session_state.psidcc)

    def query_to_bard(payload):
        bard = Bard(token=st.session_state.token, session=session)

        response = bard.get_answer(payload)
        return response

    with st.form('form_for_google_bard', clear_on_submit = True):
        user_input = st.text_input('Message: ', '')
        submitted = st.form_submit_button('Send')

    if submitted and user_input:
        output = query_to_bard(user_input)

        st.session_state.user_inputs.append(user_input)
        st.session_state.generated_responses.append(output['content'])

    if st.session_state['generated_responses']:
        for i in range(0, len(st.session_state['generated_responses']), 1):
            message(st.session_state['user_inputs'][i], is_user = True, key=str(len(st.session_state['generated_responses'])) + '_' + str(i) + '_google_bard_user')
            message(st.session_state['generated_responses'][i], key=str(len(st.session_state['generated_responses'])) + '_' + str(i) + '_google_bard')


