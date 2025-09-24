import streamlit as st
import json
import time

class Login:
    def __init__(self, timeout=3600):  # Timeout in seconds (5 minutes default)
        self.timeout = timeout
        self.user_data = self.load_user_data()
        self.session_key = "logged_in"

    def load_user_data(self):
        with open("user.json", "r") as file:
            return json.load(file)

    def login(self):
        st.title("Login")

        # Username and password fields
        username = st.text_input("Username", key="username", placeholder="Enter your username")
        password = st.text_input("Password", key="password", type="password", placeholder="Enter your password")
        login_button = st.button("Login")

        if login_button:
            user = next((u for u in self.user_data["users"] if u["username"] == username and u["password"] == password), None)
            if user:
                st.session_state[self.session_key] = {"username": username, "role": user["role"], "login_time": time.time()}
                st.success(f"Welcome, {username}!")
                st.rerun()  
                # st.experimental_rerun() 
            else:
                st.error("Invalid username or password.")

    def check_timeout(self):
        if self.session_key in st.session_state:
            login_time = st.session_state[self.session_key]["login_time"]
            if time.time() - login_time > self.timeout:
                st.warning("Session timed out. Please log in again.")
                st.session_state.pop(self.session_key, None)
                st.rerun()
                # st.experimental_rerun() 

    def logout(self):
        
        if st.button("Logout"):
            st.session_state.pop(self.session_key, None)
            st.success("You have been logged out.")
            st.rerun()
            # st.experimental_rerun() 

    def is_authenticated(self):
        return self.session_key in st.session_state

    def get_user_role(self):
        if self.is_authenticated():
            return st.session_state[self.session_key]["role"]
        return None
