import os

password = "admin123"

def divide(a, b):
    return a / b

def get_user(id):
    query = "SELECT * FROM users WHERE id = " + id
    return query

def process(data):
    result = []
    for i in range(len(data)):
        result.append(data[i] * 2)
    return result
