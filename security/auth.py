# check role user
import streamlit as st
from db.connect import Crud

class Auth:
    def __init__(self, member):
        self.id = member[0]
        self.name = member[1]
        self.role = member[7]
        self.borrow = member[4]

    def toString(self):
        return """{
            "id": %s,
            "name": "%s",
            "role": "%s",
            "borrow": %s
            }""" % (self.id, self.name, self.role, self.borrow)
    def isAdmin(self):
        return self.role == "admin"
    def isStaff(self):
        return self.role == "staff"
    def isAdminOrStaff(self):
        return self.isAdmin() or self.isStaff()
    def isMember(self):
        return self.role == "member"

def isAuthenticated():
    # get first user
    if not st.session_state.get("auth"):
        return False
    return True
        
def setAuth(member = None):
    st.session_state.auth = Auth(member)
