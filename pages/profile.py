import streamlit as st
from db.connect import Crud
from security.auth import isAuthenticated
import pandas as pd

def profile():
    if isAuthenticated():        
        st.subheader("Hello " + st.session_state.auth.name)
        st.text("Role: " + st.session_state.auth.role)
        if (st.session_state.auth.borrow):
            st.text("You can borrow")
        else:
            st.text("You can't borrow, please check if you have any book that not returned in due time")
    else:
        st.error("You are not logged in")

def history():
    ticketQuery = "SELECT book.name, ticket.borrow_date, ticket.return_date FROM ticket, book WHERE ticket.book_isbn = book.isbn AND ticket.member_id = {} LIMIT 20;".format(st.session_state.auth.id)
    st.subheader("History")
    df = pd.DataFrame(Crud.fetchAll(ticketQuery), columns=['title','borrow_date', 'return_date'])
    st.dataframe(df)

profile()
history()