import streamlit as st
import numpy as np
import pandas as pd

st.write(f"Number of spots available : {st.session_state.spots}")
st.divider()

#if "spots" not in st.session_state:
#  st.session_state.spots = 4

#spots = 0
def restore_spots():
    st.write("restoring spots...")
    st.session_state.spots = 4
    
def take_spot():
    if st.session_state.spots :
      st.session_state.spots = st.session_state.spots -1 
      st.write("taking a spot ...")
    else:
        st.write("No spots available")    

def release_spot():
    if (st.session_state.spots < 4):
      st.write("Releasing a spot...") 
      st.session_state.spots = st.session_state.spots +1
    
    
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


    

