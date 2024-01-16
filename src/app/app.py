import streamlit as st
import requests
import os
from fastapi import FastAPI, Depends
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
from pydub import AudioSegment
import base64
import json
import random
import pandas as pd

st.set_page_config(page_title="Food tracking", page_icon=":cooking:", layout="wide")


st.markdown('''<style>.css-nlntq9 a {color: #00058F;}</style>''',unsafe_allow_html=True)  # lightmode


def main():
    transcription_api_endpoint = "https://voicetracking-transcription-api-columbia-uni.dev.datasciencenonprod.us-east4.gcp.wwiops.io/"
    # if we're performing a local run, we should use a local endpoint
    if "APP_LOCAL_RUN" in os.environ:
        transcription_api_endpoint = "http://voice-tracking-transcription-api-1:8000/"

    nlp_api_endpoint = "https://voicetracking-nlp-api-columbia-uni.dev.datasciencenonprod.us-east4.gcp.wwiops.io/"
    # if we're performing a local run, we should use a local endpoint
    if "APP_LOCAL_RUN" in os.environ:
        nlp_api_endpoint = "http://voice-tracking-nlp-api-1:8080/"

    #If nlp api is called, either by voice or by text input, detected is True
    if 'detected' not in st.session_state:
        st.session_state.detected = False
    #Store the returned food dictionary from nlp api
    if 'fooddict' not in st.session_state:
        st.session_state.fooddict = dict()
    #Store the matching food names in the pkl file
    if 'matching_option' not in st.session_state:
        st.session_state.matching_option = dict()
    #Store the portion number and unit [1, 'portion'] of detected food
    if 'matching_portion' not in st.session_state:
        st.session_state.matching_portion = dict()

    if 'prev_text' not in st.session_state:
        st.session_state.prev_text = ""

    if 'prev_text_matching' not in st.session_state:
        st.session_state.prev_text_matching = dict()

    col1, col2 = st.columns([1, 1], gap="large")

    with st.sidebar:
        title = '<p style="font-family:sans-serif; color:#00058F; font-size: 24px;">Start Tracking Your Meal!</p>'
        st.markdown(title, unsafe_allow_html=True)
        st.header(":cooking: :cake: :tropical_drink: :doughnut: :fries: :tomato:")
        instructions = '<p style="font-family:sans-serif; color:#00058F; font-size: 20px;">How to use this app?</p>'
        st.markdown(instructions, unsafe_allow_html=True)
        st.write("Step 1: Record Your Audio by clicking the microphone icon!")
        st.write("Step 2: After you finish talking, click the mic icon again or simply wait for 3 seconds.")
        st.write("Step 3: After your audio is ready, the 'Detect' will be available, click the 'Detect' Button to see your result!")

    with col1:
        title_col2 = '<p style="font-family:sans-serif; color:#00058F; font-size: 36px;">Record what you eat</p>'
        st.markdown(title_col2, unsafe_allow_html=True)
        audio_bytes = audio_recorder(
            text="Click icon on the right to record",
            recording_color="#088F8F",
            neutral_color="#474A8F",
            icon_name="fa-solid fa-microphone",
            icon_size="3x",
            pause_threshold=3.0
        )

        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            st.write("Recording is successful! Click on the 'Detect' button below to see analysis on your food!")
            s = BytesIO(audio_bytes)
            encoded = base64.b64encode(audio_bytes)
            encoded_audio = encoded.decode('utf-8')

        
        title2 = '<p style="font-family:sans-serif; color:#00058F; font-size: 36px;">Querying the API</p>'
        st.markdown(title2, unsafe_allow_html=True)

        if st.button("Detect"):
            with st.spinner("Generating what you ate today..."):
                #Call transcription api, the audio is sent in the form of bytes decoded by utf-8 
                response_transcription = requests.post(os.path.join(transcription_api_endpoint, "transcribe"), json={'audio': encoded_audio})
                st.write("What you said is...")
                st.write(response_transcription.text)
                #Call nlp api
                response_nlp = requests.post(os.path.join(nlp_api_endpoint, "process-text"), json={"text": response_transcription.text})
                st.write("nlp-api response:")
                st.write("What you ate should be:", response_nlp.text)
                st.session_state.detected = True
                if response_nlp.text:
                    #The response from nlp api is a dictionary but in string form, use json loads to turn it into an actual dict
                    st.session_state.fooddict = json.loads(response_nlp.text)
                    if "matching_option" in st.session_state:
                        #clean the maching_option dict, otherwise it might store food names of both voice tracking and text input.
                        st.session_state.matching_option = dict()
                        for i in st.session_state.fooddict.keys():
                            st.session_state.matching_option[i] = ""
                    if "prev_text_matching" in st.session_state:
                        for i in st.session_state.fooddict.keys():
                            st.session_state.prev_text_matching[i] = "E.g. Apple"
                    if "matching_portion" in st.session_state:
                        st.session_state.matching_portion = dict()
                        for i in st.session_state.fooddict.keys():
                            st.session_state.matching_portion[i] = [1, 'portion', 0]
            
        if "detected" in st.session_state:
            if st.session_state.detected:
                question = 'Is this what you ate?'
                options = ["Yes!!", "No, this is not what I ate!"]

                answer = st.radio(question, options)
                # Execute different code, if choosing no, let the user input what they ate in textbox.
                if answer == "Yes!!":
                    yes_ = '<p style="font-family:sans-serif; color:#00058F; font-size: 15px;">Hooray! Stay healthy and keep tracking your meals!</p>'
                    st.markdown(yes_, unsafe_allow_html=True)
                elif answer == "No, this is not what I ate!":
                    no_ = '<p style="font-family:sans-serif; color:#00058F; font-size: 15px;">Ohno! Please try recording your voice again or type what you ate in the box below</p>'
                    st.markdown(no_, unsafe_allow_html=True)
                    # Allow users to type what they ate if voice control fails
                    default_value = "Today I ate..."
                    user_input = st.text_input("Please type what you ate here", default_value, key="recall_nlp_api")
                    if "prev_text" in st.session_state:
                        if user_input != default_value and user_input != st.session_state.prev_text:
                            st.session_state.prev_text = user_input
                            response_nlp = requests.post(os.path.join(nlp_api_endpoint, "process-text"), json={"text": user_input})
                            st.write("What you ate should be:")
                            st.write(response_nlp.text)
                            st.session_state.detected = True
                            if response_nlp.text:
                                st.session_state.fooddict = json.loads(response_nlp.text)
                                if "matching_option" in st.session_state:
                                    st.session_state.matching_option = dict()
                                    for i in st.session_state.fooddict.keys():
                                        st.session_state.matching_option[i] = ""
                                if "prev_text_matching" in st.session_state:
                                    for i in st.session_state.fooddict.keys():
                                        st.session_state.prev_text_matching[i] = "E.g. Apple"
                                if "matching_portion" in st.session_state:
                                    st.session_state.matching_portion = dict()
                                    for i in st.session_state.fooddict.keys():
                                        st.session_state.matching_portion[i] = [1, 'portion', 0]
    
    with col2:
        if "fooddict" in st.session_state:
            user_input_matching = dict()
            user_input_amount = dict()
            if st.session_state.fooddict:
                title3 = '<p style="font-family:sans-serif; color:#00058F; font-size: 36px;">Matching</p>'
                st.markdown(title3, unsafe_allow_html=True)
                st.write("What you ate should be:")
                st.write(list(st.session_state.fooddict.keys()))
                for i in st.session_state.fooddict.keys():
                    matching_question = "Please select the option below that matches '" + i + "'"            
                    with st.expander(i):                       
                        matching_options = list(st.session_state.fooddict[i].copy().keys())
                        #if there is no matching, let the user input in the textbox
                        matching_options.append("There is no matching!")
                        matching_answer = st.selectbox(matching_question, matching_options, index = 0,  key=i+'answer')
                        if matching_answer != "There is no matching!":
                            st.session_state.matching_option[i] = matching_answer
                            if "matching_portion" in st.session_state:                 
                                user_input_amount[i] = st.text_input("Please tell us the amount:", st.session_state.matching_portion[i][0], key=i+'amount') 
                                st.session_state.matching_portion[i][0] = user_input_amount[i]
                                unit_question = "Please select the unit:"                   
                                unit_options = (k[1] for k in st.session_state.fooddict[i][matching_answer])
                                unit_answer = st.selectbox(unit_question, unit_options, index = 0, key=i+'unit')
                                st.session_state.matching_portion[i][1] = unit_answer
                                score = [k[0] for k in st.session_state.fooddict[i][matching_answer] if st.session_state.matching_portion[i][1]==k[1]]
                                if score:
                                    st.session_state.matching_portion[i][2] = float(score[0]*int(st.session_state.matching_portion[i][0]))
                                else:
                                    st.session_state.matching_portion[i][2] = 0

                        else:
                            if "prev_text_matching" in st.session_state:
                                user_input_matching[i] = st.text_input("Please tell us the food:", st.session_state.prev_text_matching[i], key=i)
                                st.session_state.prev_text_matching[i] = user_input_matching[i]
                                st.session_state.matching_option[i] = user_input_matching[i] + '(There is no matching.)'
                            if "matching_portion" in st.session_state:                 
                                user_input_amount[i] = st.text_input("Please tell us the amount:", st.session_state.matching_portion[i][0], key=i+'amount') 
                                st.session_state.matching_portion[i][0] = user_input_amount[i]
                                unit_question = "Please select the unit:"                   
                                unit_options = ['portion', 'oz', 'lb', 'slice', 'cup', 'packet', 'tbsp']
                                unit_answer = st.selectbox(unit_question, unit_options, index = 0, key=i+'unit')
                                st.session_state.matching_portion[i][1] = unit_answer
                                st.session_state.matching_portion[i][2] = 0

    if st.session_state.fooddict:
        s1= '<p style="font-family:sans-serif; color:#00058F; font-size: 15px;">Final Matching should be</p>'
        st.markdown(s1,unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1], gap="large")
        final_output = dict()
        for i in st.session_state.fooddict.keys():
            final_output[i] = [st.session_state.matching_option[i], st.session_state.matching_portion[i]]
        for i in range(len(final_output.keys())):
            food = final_output[list(final_output.keys())[i]][0]
            unit = final_output[list(final_output.keys())[i]][1][0]
            portion = final_output[list(final_output.keys())[i]][1][1]
            points = final_output[list(final_output.keys())[i]][1][2]
            if i%2 == 0:
                with c1:
                    df = pd.DataFrame({'Food Name':food,'Unit':str(unit),'Portion':str(portion), 'Points':str(points)}, index=[0])
                    st.table(df)
            else:
                with c2:
                    df = pd.DataFrame({'Food Name':food,'Unit':str(unit),'Portion':str(portion), 'Points':str(points)}, index=[0])
                    st.table(df)

if __name__ == "__main__":
    main()
