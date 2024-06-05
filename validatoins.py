import re

def validate_name(name):
    errors = []
    if not name:
        errors.append("Name field is required")
    if name:
        if len(name) < 3:
            errors.append("Name should be at least 3 characters long")
    return errors
    

def validate_email(email, users):
    errors = []
    email_regex = r'.*\w@\w.*\..*\w'
    if not email:
        errors.append("Email field is required")
    if email:
        if not re.match(email_regex, email):
            errors.append("the email format is not valid")
        if email in [user[2] for user in users]:
            errors.append("This email is already in the database! Please enter a new one")
    return errors
