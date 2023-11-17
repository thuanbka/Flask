import requests
import hashlib
import sys
import os
from config import UPLOAD_DIR
from config import UPLOAD_DIR_DRIVE_ID
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def upload_to_google_drive(file):
    try:
        file_name = file.filename
        # Create a new file on Google Drive with the specified title and parent folder ID
        drive_file = drive.CreateFile({'title': file_name, 'parents': [{'id': UPLOAD_DIR_DRIVE_ID}]})
        # Upload the file content to Google Drive
        upload_folder = UPLOAD_DIR
        if os.path.exists(UPLOAD_DIR):
            upload_folder = UPLOAD_DIR
        else:
            current_directory = os.getcwd()
            upload_folder = os.path.join(current_directory, 'uploads')
        file_path = os.path.join(upload_folder, file_name)
        drive_file.SetContentFile(file_path)
        drive_file.Upload()
        # Get the file ID
        file_id = drive_file.get('id')
        # Construct the file link
        file_link = f'https://drive.google.com/file/d/{file_id}/view'
        # Now file_link contains the link to the uploaded file
        print(f'Link to the uploaded file: {file_link}')
        return True
    except Exception as ex:
        print(ex)
        return False

def upload_file(file):
    try:
        if os.path.exists(UPLOAD_DIR):
            upload_folder = UPLOAD_DIR
        else:
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
        file.save(os.path.join(upload_folder, file.filename))
        return True
    except Exception as ex:
        print(f"Error uploading file: {ex}")
        return False

def get_github_file(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as ex:
        print(ex)
        return None

def sha256_encode(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    hashed_string = sha256_hash.hexdigest()
    return hashed_string

def get_license_local(name_file):
    with open(name_file, "r", encoding='utf-8') as f:
        return f.read().replace("\n","").strip()

def get_license(license):

    github_url = "https://raw.githubusercontent.com/thuanbka/license/main/%s.txt"%(license)
    file_content = get_github_file(github_url)
    if file_content is not None:
        return file_content.replace("\n","").strip()
    else:
        return None

if __name__ == "__main__":
    number_args = len(sys.argv)
    if number_args >= 2:
        if sys.argv[1] == "check_encode_sha256":
            if number_args == 3:
                code = sys.argv[2]
                print("Encode SHA256 for '%s':"%(code))
                print(sha256_encode(code))
            else:
                print("Please enter a string which you want to encode.")
        elif sys.argv[1] == "get_license":
            if number_args == 3:
                license = sys.argv[2]
                print("License for '%s':"%(license))
                print(get_license(license))
            else:
                print("Please enter a string which you want to get license.")

    else:
        print("...................")
