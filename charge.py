import streamlit as st
import numpy as np
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

import subprocess

#from streamlit_gsheets import GSheetsConnection
#@st.cache_data
def get_sheet_data():
   scopes = ["https://www.googleapis.com/auth/spreadsheets"]
   creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
   client = gspread.authorize(creds)
   sheet_id = "1X5-Q9X9Z2IzR604BIefQfr1iRS7qmMPGbFLgBH5LBW8"
   sh = client.open_by_key(sheet_id)
   ws = []
   l_l_l = []
   for i in range(len(sh.worksheets())):
     s = sh.get_worksheet(i)
     ws.append(s)
     l_l_l.append(s.get_all_values())
   return ws, l_l_l

ws, l_l_l = get_sheet_data()

l_l = l_l_l[1]

user_q = []
for i in range(len(l_l)):
    if len(l_l[i]) > 0:
        user_q.append(l_l[i][0])

if 'selected_name' not in st.session_state : 
  st.session_state.selected_name = "None" 

if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = True

def print_avail_spot():
  st.write(f"Selected user : {st.session_state.selected_name}")
  st.write(f"Number of spots available : {st.session_state.spots}")


print("***** debug1 *****")
st.session_state['spots'] = int(ws[0].cell(1,1).value)

print(f"***** debug2 : {st.session_state.spots} *****")


#spots = 0
def add_to_queue():
    st.write("Adding to queue..")
    #ws[0].update([[4]],'A1')
    #st.session_state.spots = 4
    print("***** add_to_queue *****")
    ws[1].update([[st.session_state.selected_name]],f"A{len(l_l_l[1])+1}")
    
def take_spot():
    if st.session_state.spots > 0:
      st.session_state.spots = st.session_state.spots - 1
      ws[0].update([[st.session_state.spots]],'A1')
      st.write("taking a spot ...")
      #st.rerun()
      print("***** take_spot *****")
    else:
        st.write("No spots available")    

def release_spot():
    if (st.session_state.spots < 4):
      st.write("Releasing a spot...") 
      st.session_state.spots = st.session_state.spots +1 
      ws[0].update([[st.session_state.spots]],'A1')
      print("***** release_spot *****")
    
col1,col2,col3 = st.columns(3)

with col1:
  st.button("Take a spot",disabled=(st.session_state.selected_name == "None"),on_click=take_spot)

with col2:
  st.button("Release a spot",disabled=(st.session_state.selected_name == "None"),on_click=release_spot)

with col3:
  st.button("Add to queue",disabled=(st.session_state.selected_name == "None"),on_click=add_to_queue)



#get users from worksheet#2
names = []
for i in range(len(l_l_l[2])):
  names.append(l_l_l[2][i][0])

st.selectbox("Identify yourself",names, key="selected_name")

print_avail_spot()

st.divider()
st.caption("Current wait queue.. ")

df = pd.DataFrame(
     {
         "Names": user_q 
     }
)

st.table(df)
st.divider()


with st.form("my_form"):
    row = st.columns([1,2,2])
    name = row[0].text_input("Name")
    email = row[1].text_input("Email")
    ph = row[2].text_input("Phone# (opt)")
    submitted = st.form_submit_button("Add new user")
    if submitted:
      st.write(f"Added new user : {name} {email} {ph} ")
      entry = [name,email,ph]
      ws[2].update([entry],f"A{len(l_l_l[2])+1}")

