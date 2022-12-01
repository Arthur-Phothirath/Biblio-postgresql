import datetime
import streamlit as st
from db.connect import Crud

def createTicket(isbn):
    ticketQuery = "INSERT INTO ticket (member_id, book_isbn, quantity,borrow_date) VALUES ({}, {}, {}, '{}');".format(st.session_state.auth.id, isbn, 1,datetime.date.today())
    Crud.mutation(ticketQuery)
    
def returnTicket(isbn):
    ticketQuery = "UPDATE ticket SET return_date = '{}' WHERE book_isbn = {} AND member_id = {} AND return_date IS NULL;".format(datetime.date.today(), isbn, st.session_state.auth.id)
    Crud.mutation(ticketQuery)
    print(ticketQuery)