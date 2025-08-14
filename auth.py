import streamlit as st
import bcrypt
import pickle
import os
from datetime import datetime

USERS_FILE = "users.pkl"
LOG_FILE = "login_logs.csv"

# Load existing users
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "rb") as f:
            return pickle.load(f)
    return {}

# Save users
def save_users(users):
    with open(USERS_FILE, "wb") as f:
        pickle.dump(users, f)

# Log successful login
def log_login(username):
    with open(LOG_FILE, "a") as f:
        f.write(f"{username},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Signup function
def signup(username, password):
    users = load_users()
    if username in users:
        st.error("Username already exists!")
        return False
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[username] = hashed_pw
    save_users(users)
    st.success("Account created successfully!")
    return True

# Login function
def login(username, password):
    users = load_users()
    if username in users and bcrypt.checkpw(password.encode(), users[username]):
        log_login(username)
        return True
    return False

# Authentication UI
def auth_ui():
    st.sidebar.title("User Authentication")
    choice = st.sidebar.radio("Choose Action", ["Login", "Sign Up"])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.sidebar.button("Create Account"):
            signup(username, password)

    elif choice == "Login":
        if st.sidebar.button("Login"):
            if login(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(f"Welcome {username}!")
            else:
                st.error("Invalid username or password")
