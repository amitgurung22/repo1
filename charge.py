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

spots = 0
ws = get_sheet_data()

print("***** debug1 *****")
spots = int(ws[0].cell(1,1).value)
print(f"***** debug2 : {spots} *****")
st.session_state['spots'] = spots
st.write(f"Number of spots available : {spots}")

#spots = 0
def restore_spots():
    st.write("restoring spots...")
    ws[0].update([[4]],'A1')
    
def take_spot():
    if st.session_state['spots'] > 0:
      st.session_state['spots'] = st.session_state['spots'] - 1
      #spots = spots -1 
      #ws[0].update([[spots]],'A1')
      ws[0].update([[st.session_state['spots']]],'A1')
      st.write("taking a spot ...")
      st.rerun()
    else:
        st.write("No spots available")    

def release_spot():
    if (spots < 4):
      st.write("Releasing a spot...") 
      spots = spots +1 
      ws[0].update([[spots]],'A1')
    
    
t = st.button("take a spot")
r = st.button("release a spot")
res = st.button("restore all spots")


if t :
    take_spot()
if r :
    release_spot()
if res:
    restore_spots()
    
    

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
