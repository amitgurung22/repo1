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
   for i in range(len(sh.worksheets())):
     ws.append(sh.get_worksheet(i))
   return ws

ws = get_sheet_data()


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
    ws[0].update([[4]],'A1')
    st.session_state.spots = 4
    print("***** add_to_queue *****")
    
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
  t = st.button("Take a spot",disabled=(st.session_state.selected_name == "None"))

with col2:
  r = st.button("Release a spot",disabled=(st.session_state.selected_name == "None"))

with col3:
  res = st.button("Add to queue",disabled=(st.session_state.selected_name == "None"))



if t :
    take_spot()
if r :
    release_spot()
if res:
    add_to_queue()
    
names = ["Amit Gurung", "Aarav", "Tvisha"]

st.selectbox("Identify yourself",names, key="selected_name")

print_avail_spot()

st.caption("QUEUE")
st.divider()
for i in range(10):
    st.write(f"{i}:user{i}")
st.divider()

## Create a connection object.
#conn = st.connection("gsheets", type=GSheetsConnection)
#
#df = conn.read()
#
#df 

# Print results.
#for row in df.itertuples():
#    st.write(f"{row.name} has a :{row.pet}:")


#url = "https://docs.google.com/document/d/1H7qsqs7VtsRD0XrndYXSSYfgTDzdhusqojFwOzG1iUw/edit?usp=drivesdk"
#resp = requests.get(url)
#
#with open("d.txt","wb") as f:
#    f.write(resp.content)
#
#result = subprocess.run(['cat', 'd.txt'],capture_outputs=True,text=True)
#
#st.write(result.stdout)



# Initialize connection.
#conn = st.connection('mysql', type='sql')
#
## Perform query.
#df = conn.query('SELECT * from mytable;', ttl=600)
#
## Print results.
#for row in df.itertuples():
#    st.write(f"{row.name} has a :{row.pet}:")
