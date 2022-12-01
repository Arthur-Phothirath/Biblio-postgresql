import streamlit as st
from security.auth import isAuthenticated

if isAuthenticated():
    
    if st.session_state.auth.isAdmin():
        st.success("You are admin")
    elif st.session_state.auth.isStaff():
        st.success("You are staff")
    elif st.session_state.auth.isMember():
        st.success("You are member")
        
    st.subheader("Hello " + st.session_state.auth.name)
    st.text("Your role is " + st.session_state.auth.role)
    st.text("Your borrow is " + str(st.session_state.auth.borrow))
    st.text("Your id is " + str(st.session_state.auth.id))
    st.write(st.session_state.auth.toString())
else:
    st.error("You are not logged in")
