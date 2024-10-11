import requests, os, sys
from . import constants

def generate_auth_code():
    url = f"https://api.pcloud.com/userinfo?getauth=1&username={constants.username}&password={constants.password}"
    response = requests.request("GET", url)
    if "error" in response.json():
        print("[Auth] - Error generating auth code. Bad credentials.")
        sys.exit(1)
    auth_code = response.json().get("auth")
    print("[Auth] - Generated a new auth code")
    return auth_code

def save_auth_code(auth_code):
    file_path = __get_filepath()
    with open(file_path, "w") as f:
        f.write(auth_code)
    
def get_auth_code():
    file_path = __get_filepath()
    with open(file_path, "r") as f:
        return f.read()
    
def __get_filepath():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "auth_code.sam"
    file_path = os.path.join(script_dir, filename)

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("")
    
    return file_path

def get_active_auth_code(runtimes=0):   
    saved_auth_code = get_auth_code()
    
    if user_is_auth(saved_auth_code):
        return saved_auth_code
    else:
        new_auth_code = generate_auth_code()
        save_auth_code(new_auth_code)
        if runtimes > 2:
            raise Exception("[Auth] Trouble getting new auth code. Check credentials.")
        return get_active_auth_code(runtimes + 1)

def user_is_auth(auth_code):
    response = requests.request("GET", f"https://api.pcloud.com/userinfo?auth={auth_code}")
    if response.text.__contains__("error"):
        return False
    else:
        return True