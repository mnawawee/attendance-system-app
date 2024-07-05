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
tab1, tab2, tab3 = st.tabs(['Registered Data','Logs','Attendance Report'])

with tab1:
    if st.button('Refresh Data'):
    # Retrive the data from Redis Database
     with st.spinner('Retriving Data from Redis Db..'):
        redis_face_db = face_rec.retrive_data(name='academy:register')
        st.dataframe(redis_face_db[['Name','Role']])

with tab2:
    if st.button('Refresh Logs'):
        st.write(load_logs(name=name))


with tab3:
   st.subheader('Attendance Report')

    # logs
   logs_list =load_logs(name=name)

   # step 1: covrt the logs dat in list of bytes into list of string
   convert_byte_to_string = lambda x: x.decode('utf-8')
   logs_list_string =list(map(convert_byte_to_string,logs_list))

   # 2slipt
   split_string = lambda x: x.split('@')
   logs_nested_list = list(map(split_string,logs_list_string))
   # cvrt
   logs_df =pd.DataFrame(logs_nested_list, columns= ['Name','Role','Timestamp'])

   # 3time anylsis
   logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])
   logs_df['Date'] = logs_df['Timestamp'].df.date

   # 3.1 cal time in outtime
   #timein
   #timeout
   report_df = logs_df.groupby(by=['Date','Name','Role']).agg(
      in_time = pd.NamedAgg('Timestamp','min'), #in time
      out_time = pd.NamedAgg('Timestamp','max') #out time
   ).reset_index()

   report_df['in_time'] = pd.to_datetime(report_df['in_time'])
   report_df['out_time'] = pd.to_datetime(report_df['out_time'])

   report_df['Duration'] = report_df['out_time'] - report_df ['in_time']

   #step mark prent or absent
   all_dates = report_df['Date'].unique()
   name_role =report_df[['Name','Role']].drop_duplicates().values.tolist()
    
   date_name_rol_zip = []
   for dt in all_dates:
       for name, role in name_role:
           date_name_rol_zip.append([dt,name,role])
   date_name_rol_zip_df = pd.DataFrame(date_name_rol_zip,columns=['Date','Name','Role'])

   date_name_rol_zip_df = pd.merge(date_name_rol_zip, report_df, how='left',on=['Date','Name','Role'])
        

   

    #duration
    #hours
   date_name_rol_zip_df['Duration_seconds'] = date_name_rol_zip_df['Duration'].dt.seconds
   date_name_rol_zip_df['Duration_hours'] = date_name_rol_zip_df['Duration_seconds'] / (60*60)
   
   def status_marker(x):
      
      if pd.Series(x).isnull().all():
         return 'Absent'
      elif x >= 0 and x < 1:
         return 'Absebt (Less than 1 hrs)'
      elif x >= 1 and x < 4:
         return 'Half day (Less than 4 hrs)'
      elif x >= 4 and x < 6:
         return 'Half day'
      elif x >= 6:
         return 'Present'
      
   date_name_rol_zip_df['Status'] =date_name_rol_zip_df['Duration_hours'].apply(status_marker)     

         

   st.dataframe(date_name_rol_zip_df)





