import streamlit as st
from Home import face_rec
st.set_page_config(page_title='Reporting',layout='wide')
st.subheader('Reporting')


#Retrive logs data and show In report.py
#exract data from rd list
name = 'attendance:logs'
def load_logs(name,end=-1):
    logs_list = face_rec.r.lrange(name,start=0,end=end)# extract all data from rd database
    return logs_list
#tabs to show the infor
tab1, tab2 = st.tabs(['Registered Data','Logs'])

with tab1:
    if st.button('Refresh Data'):
    # Retrive the data from Redis Database
     with st.spinner('Retriving Data from Redis Db..'):
        redis_face_db = face_rec.retrive_data(name='academy:register')
        st.dataframe(redis_face_db[['Name','Role']])

with tab2:
    if st.button('Refresh Logs'):
        st.write(load_logs(name=name))

