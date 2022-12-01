import datetime
import streamlit as st
import pandas as pd
from db.connect import Crud
from security.auth import isAuthenticated
from utils.ticket import createTicket, returnTicket
from utils.blockBorrow import blockBorrow

class Book:
    def __init__(self, book):
        self.title = book[0]
        self.author = book[1]
        self.year = book[2]
        self.isbn = book[3]
        self.quantity = book[4]



def booksPage():
  # List des livres 
  def bookList():
      st.title("Book List")
      search = st.text_input("Search")
      query = "SELECT book.name, book.author, book.publish_date, book.isbn, book.quantity, category.name FROM book, category WHERE book.name LIKE '%{}%' OR  category.name = '%{}%'".format(search, search)
      print("Query: ", query)
      books = Crud().fetchAll(query)
      df = pd.DataFrame(books, columns=['title', 'author', 'year', 'isbn', 'quantity', 'category'])
      st.dataframe(df)

  if isAuthenticated() and st.session_state.auth.isAdmin():
     # Rajouter un livre 
    def addBook():
        st.title("Add Book")
        name = st.text_input("Title")
        author = st.text_input("Author")
        publish_date = st.date_input("Publish Date")
        isbn = st.number_input("ISBN", min_value=1000000000,  max_value=9999999999999)
        quantity = st.number_input("Quantity", min_value=1,  max_value=1000, value=1)
        category = st.selectbox("Category", Crud().fetchAll("SELECT name FROM category"))
        description = st.text_area("Description")
        if st.button("Add"):
          if Crud.fetchOne("SELECT * FROM book WHERE isbn = {};".format(isbn)) is not None:
            st.warning("Book already exists")
            return
          query = "INSERT INTO book (name, author, publish_date, isbn, quantity) VALUES ('{}', '{}', '{}', '{}', {});".format(name, author, publish_date, isbn, quantity)
          Crud.mutation(query)
          queryCatgory = "INSERT INTO category (name, book_isbn, description) VALUES ('{}', '{}', '{}');".format(category, isbn, description)
          Crud.mutation(queryCatgory)
          st.info("Book added")

    # Mettre à jour le livre
    def updateBook():
      st.title("Update Book")
      isbn = st.number_input("ISBN", min_value=1000000000,  max_value=9999999999999)
      quantity = st.number_input("Quantity", min_value=1,  max_value=1000, value=1)
      if st.button("Update"):
        query = "UPDATE book SET quantity = {} WHERE isbn = {};".format(quantity, isbn)
        Crud.mutation(query)
        st.info("Book updated")

     # Supprimer un book
    def deleteBook():
      st.title("Delete Book")
      isbn = st.number_input("ISBN", min_value=1000000000,  max_value=9999999999999)
      if st.button("Delete"):
        if Crud.fetchOne("SELECT * FROM book WHERE isbn = {};".format(isbn)) is None:
          st.warning("Book does not exist")
          return
        query = "DELETE FROM book WHERE isbn = {};".format(isbn)
        Crud.mutation(query)
        st.info("Book deleted")

  #  Emprunter un livre
  def borrowBook():
    if blockBorrow(st.session_state.auth.id) is True:
      st.error("You can't borrow, please check if you have any book that not returned in due time")
      return
    st.title("Borrow Book")
    isbn = st.number_input("ISBN", min_value=1,  max_value=9999999999999)
    if st.button("Borrow"):
      if st.session_state.auth.borrow == False:
        st.warning("You are not allowed to borrow book")
        return
      if Crud.fetchOne("SELECT quantity FROM book WHERE isbn = {};".format(isbn))[0] < 1:
        st.warning("Book is not available")
        return
      query = "UPDATE book SET quantity = quantity - 1 WHERE isbn = {};".format(isbn)
      Crud.mutation(query)
      st.info("Book borrowed")
      createTicket(isbn)
      
  # Rendre un livre
  def returnBook():
    st.title("Return Book")
    isbn = st.number_input("ISBN", min_value=1,  max_value=9999999999999)
    if st.button("Return"):
      # if not st.session_state.auth.isMember():
      #   st.warning("You are not authorized to return book")
      #   return
      query = "UPDATE book SET quantity = quantity + 1 WHERE isbn = {};".format(isbn)
      Crud.mutation(query)
      st.info("Book returned")
      returnTicket(isbn)
    history = "SELECT * FROM ticket WHERE member_id ={};".format(st.session_state.auth.id)
    history = Crud.fetchAll(history)
    df = pd.DataFrame(history, columns=['id', 'member_id', 'book_isbn', 'quantity','borrow_date', 'return_date'])
    st.dataframe(df)
    
  if st.session_state.get("page") is None:
    st.session_state["page"] = "allBooks"

  # menu livre
  if st.sidebar.button("Show All Books"):
    st.session_state["page"] = "allBooks"
  if isAuthenticated():
    if st.session_state.auth.isAdmin():
      if st.sidebar.button("Add Book"):
        st.session_state["page"] = "addBook"
      if st.sidebar.button("Update Book"):
        st.session_state["page"] = "updateBook"
      if st.sidebar.button("Delete Book"):
        st.session_state["page"] = "deleteBook"
      if st.sidebar.button("Return Book"):
          st.session_state["page"] = "returnBook"
    if st.session_state.auth.isAdmin() or st.session_state.auth.isMember():
      if st.sidebar.button("Borrow Book"):
        st.session_state["page"] = "borrowBook"

  if st.session_state["page"] == "allBooks":
    bookList()
  if st.session_state["page"] == "addBook":
    addBook()
  if st.session_state["page"] == "updateBook":
    updateBook()
    bookList()
  if st.session_state["page"] == "deleteBook":
    deleteBook()
    bookList()
  if st.session_state["page"] == "borrowBook":
    borrowBook()
    bookList()
  if st.session_state["page"] == "returnBook":
    returnBook()
    
booksPage()