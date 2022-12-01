import streamlit as st
from db.connect import Crud
from security.auth import setAuth
from utils.checkBorrow import checkBorrow

# login page
def login():
    st.title("Login")
    name = st.text_input("name")
    password = st.text_input("Password", type='password')
    query = "SELECT * FROM member, role WHERE  member.name = '{}' AND member.password = '{}' AND id = member_id;".format(name, password)
    if st.button("Login"):
        userFetched = Crud.fetchOne(query)
        if userFetched is not None:
            st.success("Logged in as {} ".format(name))
            setAuth(userFetched)
            checkBorrow(userFetched[0])
        else:
            st.warning("Incorrect name/Password")

def autoLogin():
    if st.button("Auto Login member"):
        query = "SELECT * FROM member, role WHERE  member.name = 'Mary' AND member.password = '1234' AND id = member_id;"
        userFetched = Crud.fetchOne(query)
        if userFetched is not None:
            setAuth(userFetched)
            checkBorrow(userFetched[0])
    if st.button("Auto Login admin"):
        query = "SELECT * FROM member, role WHERE  member.name = 'John' AND member.password = '1234' AND id = member_id;"
        userFetched = Crud.fetchOne(query)
        if userFetched is not None:
            setAuth(userFetched)
            checkBorrow(userFetched[0])
    st.info("Login success")
    
login()
autoLogin()
