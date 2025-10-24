import random
import string

def random_username(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def random_email():
    return f"{random_username()}@example.com"
