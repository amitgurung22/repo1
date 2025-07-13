
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
  st.divider()
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
      str = f"If you are not in a position to take the spot immediately kindly inform {user_q[1]} who is next in queue" if (len(user_q) > 1) else "" 
      send_email(email_dict[user_q[0]],"Tesla Charging spot available, your are 1st on waiting list","Kindly use the spot. " + str)
    if (len(user_q)>1) :
      send_email(email_dict[user_q[1]],"Tesla Charging spot available, your are 2nd on wating list",f"{user_q[0]} is ahead of you")

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
  
  print(f"Email sent! to {receiver_email} sub:{sub} body:{body}.. ")

def send_test_email():
  send_email(email_dict[st.session_state.selected_name],"This is a test email from from ev charing site","")

tab1, tab2 = st.tabs(["Main","Instructions"])

with tab1:
  st.title("Tesla Las Cimas Ev :material/electric_car: Charging Reservation")
  st.divider()
  st.markdown(":red[:small[*****    Pls refresh before any action to use up-to-date information        ****]]")
  
  
  col1,col2,col3,col4 = st.columns(4)
  
  with col1:
    st.button("Take spot",disabled=(st.session_state.selected_name == "None"),on_click=take_spot)
  
  with col2:
    st.button("Release spot",disabled=(st.session_state.selected_name == "None"),on_click=release_spot)
  
  with col3:
      st.button("Add to queue",disabled=(st.session_state.selected_name == "None"),on_click=add_to_queue)
  #  st.button("Add to queue",disabled=(st.session_state.selected_name == "None"),on_click=add_to_queue)
  
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
  
  st.divider()
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
  
  with st.expander("Add/modify user info"): 
    with st.form("my_form"):
        row = st.columns([1,2,2])
        name = row[0].text_input("Name")
        email = row[1].text_input("Email")
        ph = row[2].text_input("Phone# (opt)")
        submitted = st.form_submit_button("Add/modify user info")
        if submitted:
          st.write(f"Added new user : {name} {email} {ph} ")
          entry = [name,email,ph]
          cell = ws[2].find(name)
          if (cell) :
              ws[2].update([entry],f"A{cell.row}")
          else:
              ws[2].update([entry],f"A{len(l_l_l[2])+1}")
  
  
  
  with st.expander("Maintenance"):
    admin_psswd = st.text_input("Admin password")
    with st.form("form2"):
      #b1 = st.button("Clear queue",disabled=(admin_psswd != "1234"))
      upd_spots =  st.number_input("Enter # of spots available",disabled=(admin_psswd != "1234"))
      c_val = st.checkbox("Clear queue",disabled=(admin_psswd != "1234"))
      sub1 = st.form_submit_button("Apply",disabled=(admin_psswd != "1234"))
      if sub1:
        ws[0].update([[upd_spots]],'A1')
        print("updating slots to {upd_spots}")
        if c_val:
          ws[1].delete_rows(1,len(l_l_l[1]))
          user_q = []
        st.rerun()
  
  
  st.markdown(":material/article_person: :blue[Created by : Amit Gurung amitgurung22@gmail.com] ")

with tab2:
    st.markdown("""
       ### Instructions :material/quick_reference_all:
       * Current # of empty charging spots and current waiting queue can viewed on the main page. Always refresh to get up-to-date information 
       * For any other action, user needs to identify them by selecting their name from the "Identify yourself dropdown (or can type name there)
       * Once user is identified, then other action button buttons will become visible
       * Press "Take spot" button once you take a open spot and plug your car for charging
       * Press "Release spot" button once you release a spot (or are enroute to release a spot)
       * When # of spots == 0, press "Add to queue" button to add yourself to the waiting queue. Your name should be added to the wait queue in order
       * If for some reason you want to quit the queue, press "Quit queue button"
       * When # of empty spots == 0 and there are people in the wait queue, if a person (occupying one of the spots) presses "Release spot" then an email is sent to the 1st and 2nd person in wait queue"
       * Notification Email is sent from my gmail account with id amitgurung22@gmail.com, pls check spam folder for email received. Try the test email button at the bottom to try if a test email can be received on your email id. **Pls identify yourself before pressing this button**"
       * Your preferred email id can be changed by click "Add/modify user info"
         * If order to modify existing user info, pls match Name precisely
         * New user info can also be added using the same form
    """)
    st.button("Send test :email: ",on_click=send_test_email)
    st.markdown("""

       ### Limitations :material/production_quantity_limits:
       * Google sheet API allows limited number of api access per minute. If multiple users are interacting at the same time you may run into :red["Quota exceeded for quota metric 'Read requests' and limit.."] Please wait a minute and refresh, it should work
       * Currently this website is hosted on a local machine with forwarding. If the machine is rebooted, the link to this site will change, but will share this in time
       * No real user authentication (as wanted to make this simple), this works on trust that people are doing the right thing
       * Created over a weekend, so may have bugs. pls report to me : amitgurung22@gmail.com  any issues you encounter

       ### Future work :material/rocket_launch:
       * Host this website on streamlit cloud, so that there is no dependency on a local machine working
       * Move to text message based notification (instead of :email: ), but this may add :heavy_dollar_sign:

    """)

#google material icon
#https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded&selected=Material+Symbols+Rounded:article_person:FILL@0;wght@400;GRAD@0;opsz@24&icon.size=24&icon.color=%231f1f1f
#streamlit emoji
#https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
