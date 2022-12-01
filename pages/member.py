import streamlit as st
from db.connect import Crud
import pandas as pd
from security.auth import isAuthenticated

# User list
if isAuthenticated() and st.session_state.auth.isAdmin():
  def userList():
      st.title("Member List")
      memberList = Crud.fetchAll("SELECT member.id, member.name, member.can_borrow, role.name, member.ban from member, role WHERE id = member_id LIMIT 20;")
      df = pd.DataFrame(memberList, columns=['id','name','can_borrow', 'role', 'ban'])
      st.dataframe(df)
      id = st.text_input("User Id")
      ban = st.checkbox("Ban")
      if st.button("Update"):
          query = "UPDATE member SET ban = {} WHERE id = '{}';".format(ban, id)
          Crud.mutation(query)
          st.info("Member updated")
    
  userList()
else:
  st.info("You are not allowed to access this page")