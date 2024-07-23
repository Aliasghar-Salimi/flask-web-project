import re

def validate_username(username):
    errors = []
    if not username:
        errors.append("Name field is required")
    if username:
        if len(username) < 5:
            errors.append("Userame should be at least 3 characters long")
        if len(username) > 50:
            errors.append("Userame should not be more than 50 characters long")
        " ".join(username.split())
    return errors
    


def validate_first_name(name):
    errors = []
    if not name:
        errors.append("first name field is required")
    if name:
        if len(name) < 3:
            errors.append("first name should be at least 3 characters long")
        if len(name) > 100:
            errors.append("first name should not be more than 100 characters long")
        " ".join(name.split())
    return errors
    
def validate_last_name(name):
    errors = []
    if not name:
        errors.append("last name field is required")
    if name:
        if len(name) < 3:
            errors.append("last name should be at least 3 characters long")
        if len(name) > 100:
            errors.append("last name should not be more than 100 characters long")
        " ".join(name.split())
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
        " ".join(email.split())
    return errors


def validate_birthdate(date):
    errors = []
    date_regex = r"\d\d\/\d\d\/\d\d\d\d"
    if not date:
        errors.append("birth date field is required")
    if date:
        if not re.match(date_regex, date):
            errors.append("the date format is not valid")
    return errors

def  validate_gender(gender):
    errors = []
    gender_regex = r"[M, F]"
    if not gender:
        errors.append("gender field is required")
    if gender:
        if not re.match(gender_regex, gender):
            errors.append("gender sould be M for male or F for female")
    return errors

def validate_password(password):
    errors = list()
    password_regex = r"[A-Za-z0-9@#$%^&+=]{8,}" # Minimum eight characters, at least one uppercase letter, one lowercase letter and one number
    

    if not re.match(password_regex, password):
        errors.append("""Please enter a stronger password, it should be minimum 
                      eight characters, at least one uppercase letter, one lowercase
                      letter and one number""") 
        " ".join(password.split())
    return errors

def validate_phone(phone):
    errors = []
    phone_regex = r"^(\d{4}[\-,\.]\d{3}[\-,\.]\d{4}|\d{11})$"
    if phone:
        if not re.match(phone_regex, phone):
            errors.append("the phone format is not valid")
        " ".join(phone.split())
    return errors


