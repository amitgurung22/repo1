
#Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:153769133042'.

import streamlit as st
import re
import numpy as np
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

import subprocess

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

#user queue
l_l = l_l_l[1]
print(l_l)
user_q = []

for i in range(len(l_l)):
    if len(l_l[i]) > 0:
        nm = l_l[i][0]
        if (re.match(r"\w",nm)):
          user_q.append(l_l[i][0])



if 'selected_name' not in st.session_state : 
  st.session_state.selected_name = "None" 

if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = True

def print_avail_spot():
  st.write(f"Selected user : {st.session_state.selected_name}")
  st.subheader(f"Number of spots available : {st.session_state.spots}")


print("***** debug1 *****")
st.session_state['spots'] = int(ws[0].cell(1,1).value)

print(f"***** debug2 : {st.session_state.spots} *****")

def rm_user_from_q():
  if (st.session_state.selected_name in user_q):
    ws[1].delete_rows(1,len(l_l_l[1]))
    user_q.remove(st.session_state.selected_name)
    n_n = []
    for i in range(len(user_q)):
        l = []
        l.append(user_q[i])
        n_n.append(l)
    ws[1].update(n_n,'A1')
    print(n_n)


#spots = 0
def add_to_queue():
    st.write("Adding to queue..")
    #ws[0].update([[4]],'A1')
    #st.session_state.spots = 4
    print("***** add_to_queue *****")
    ws[1].update([[st.session_state.selected_name]],f"A{len(l_l_l[1])+1}")

#reduce the # of open spots
#remove user from user queue
#todo if there is waiting list then the user should be the top of the list
def take_spot():
    if st.session_state.spots > 0:
      st.session_state.spots = st.session_state.spots - 1
      ws[0].update([[st.session_state.spots]],'A1')
      st.write("taking a spot ...")
      #st.rerun()
      print("***** take_spot *****")
      rm_user_from_q()
    else:
        st.write("No spots available")    

#increase the #of open spots
#email the top 2 people in queue about slot
def release_spot():
    if (st.session_state.spots < 4):
      st.write("Releasing a spot...") 
      st.session_state.spots = st.session_state.spots +1 
      ws[0].update([[st.session_state.spots]],'A1')
      print("***** release_spot *****")
    if (len(user_q)) :
      send_email(email_dict[user_q[0]],"Tesla Charging spot available, your are 1st on waiting list","Kindly use the spot")
    if (len(user_q)>1) :
      send_email(email_dict[user_q[1]],"Tesla Charging spot available, your are 2nd on wating list","user_q[0] is ahead of you")

def quit_queue():
  print("quit queue")
  #cell = ws[1].find(st.session_state.selected_name)
  #print(f"found {st.session_state.selected_name} on {cell.row}:{cell.col}")
  rm_user_from_q()
  

def send_email(to_email,sub,body):
  # Gmail credentials
  sender_email = "amitgurung22@gmail.com"
  app_password = "qzwo wogb vkxq hhdr"
  receiver_email = to_email
  
  # Create message
  msg = MIMEMultipart()
  msg['From'] = sender_email
  msg['To'] = receiver_email
  msg['Subject'] = sub
  
  msg.attach(MIMEText(body, 'plain'))
  
  # Send email via Gmail SMTP
  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
      server.login(sender_email, app_password)
      server.send_message(msg)
  
  print(f"Email sent! to {sender_email} sub:{sub} body:{body}.. ")


col1,col2,col3,col4 = st.columns(4)

with col1:
  st.button("Take a spot",disabled=(st.session_state.selected_name == "None"),on_click=take_spot)

with col2:
  st.button("Release a spot",disabled=(st.session_state.selected_name == "None"),on_click=release_spot)

with col3:
  st.button("Add to queue",disabled=(st.session_state.selected_name == "None"),on_click=add_to_queue)

with col4:
    st.button("Quit queue",disabled=(st.session_state.selected_name == "None"),on_click=quit_queue)


#get users from worksheet#2
names = []
email_dict = dict()

for i in range(len(l_l_l[2])):
  nm = l_l_l[2][i][0]
  em = l_l_l[2][i][1]
  names.append(nm)
  email_dict[nm] = em

st.selectbox("Identify yourself",names, key="selected_name")

print_avail_spot()

st.divider()
st.subheader("Current wait queue.. ")


df = pd.DataFrame(
     {
         "Name": user_q 
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



with st.expander("Maintenance"):
  admin_psswd = st.text_input("Admin password")
  with st.form("form2"):
    #b1 = st.button("Clear queue",disabled=(admin_psswd != "1234"))
    upd_spots =  st.number_input("Enter # of spots available",disabled=(admin_psswd != "1234"))
    c_val = st.checkbox("Clear queue",disabled=(admin_psswd != "1234"))
    sub1 = st.form_submit_button("Apply")
    if sub1:
      ws[0].update([[upd_spots]],'A1')
      print("updating slots to {upd_spots}")
      if c_val:
        ws[1].delete_rows(1,len(l_l_l[1]))
        user_q = []
      st.rerun()



