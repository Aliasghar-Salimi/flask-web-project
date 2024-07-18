import random



# Generate a temporary code to send in email
def generate_code():
    code = random.randrange(0000,9999)
    return code

# This function removes the type and the binary part of file names
def name_creater(user_files, user_id):
    file_names = []
    for files in user_files[user_id]:
        pattern1 = "b'"
        pattern2 = "\\..*"
        text = str(files)
        import re
        text = re.sub(pattern1, "", text)
        text = re.sub(pattern2, "", text)
        file_names.append(text)
    return file_names


# And this one just removes the binary part
def binary_remove(user_files, user_id):
    file_names = []
    for files in user_files[user_id]:
        pattern1 = "b'"
        text = str(files)
        import re
        text = re.sub(pattern1, "", text)
        text = text.replace("'", "")
        file_names.append(text)
    return file_names
