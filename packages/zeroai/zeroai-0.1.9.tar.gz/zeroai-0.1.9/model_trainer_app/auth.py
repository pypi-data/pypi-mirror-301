# model_trainer_app/auth.py

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash



auth = HTTPBasicAuth()

# In a production environment, consider storing users securely
users = {
    "admin": generate_password_hash("admin_password"),
    # Add more users as needed
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None
