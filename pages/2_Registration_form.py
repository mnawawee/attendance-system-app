import streamlit as st
from Home import face_rec
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

# st.set_page_config(page_title='Registration Form')
st.subheader('Registration Form')

# init registration form
registration_form = face_rec.RegistrationForm()

#step 1 : collect person name and unit
person_name = st.text_input(label='Official Name', placeholder='eg. MY Nawawi')
role = st.selectbox(label='Select Unit',placeholder='choose unit',options=('Software',
                                                 'Geospatial',
                                                 'Risk Management',
                                                 'NII',
                                                 'Business Process',
                                                 'Networking',
                                                 'Cyber Security',
                                                 'Server and Cloud',
                                                 'Secretariat',
                                                 'Data Harmonization',
                                                 'Project Documentation'
                                                ))

#step 2: collect facial embeddin
def video_callback_func(frame):
    img = frame.to_ndarray(format="bgr24") # 3diemen arry bgr
    reg_img, embedding = registration_form.get_embedding(img)
    #two step process 
    #1st step save data into local computer txt
    if embedding is not None:
        with open('face_embedding.txt',mode='ab') as f:
            np.savetxt(f,embedding)
            
    return av.VideoFrame.from_ndarray(reg_img,format='bgr24')

webrtc_streamer(key='registration',video_frame_callback=video_callback_func,
 rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }                
                )
# step 3: save data to database
if st.button('Submit'):
    return_val = registration_form.save_data_in_databes_db(person_name,role)
    if return_val == True:
        st.success(f"{person_name} registered sucessfully")
    elif return_val == 'name_false':
        st.error('Please enter your name: Name cannot be empty')

    elif return_val == 'file_false':
        st.error('Please upload your face image')