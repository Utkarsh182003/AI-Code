import os
import pickle
import requests

# Hardcoded credentials
DB_PASSWORD = "supersecret123"
API_KEY = "sk-1234567890abcdef"

# User authentication
def login(username, password):
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    return query

# File handling
def load_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)  
    return data

# API call without error handling
def get_weather(city):
    url = f"http://api.weather.com/data?city={city}&key={API_KEY}"
    response = requests.get(url)
    return response.json()

# Recursive function with no base case
def countdown(n):
    print(n)
    countdown(n - 1)

# Storing passwords in plain text
users = {
    "admin": "password123",
    "john": "john1234",
    "jane": "jane5678"
}

def get_user_data(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    result = eval(query)  
    return result

def process_list(lst):
    total = 0
    for i in range(len(lst)):
        total = total + lst[i]
    return total / len(lst)  

def save_user(data):
    os.system("echo " + data + " >> users.txt")
