import sys, os
from . import download, upload, auth

def show_help():
    help_text = """
    Usage: mp3-pcloud-cli <url> [--help] [--setup]

    Options:
    <url>                Youtube URL to download audio from.
    --help               Show this help message.
    --setup              Set up this mp3-pcloud-cli with the given credentials. 
    --tutorial           Show pCloud setup tutorial.
    
    Setup Usage (see --tutorial for more info):
    --setup <username> <password> <pcloud_folder_id> <pcloud_folder_code> 

    username:            Your pCloud username. 
    password:            Your pCloud password. (stored in plain text so use a dedicated account)
    pcloud_folder_id:    pCloud folder ID network inspection.
    pcloud_folder_code:  pCloud folder code from shared link.
    """
    print(help_text)

def show_pcloud_tutorial():
    tutorial_text = """
    How to get pCloud folder ID and code:
    1. Create a folder on your main pCloud account.
    2. Share the folder to anyone. Upload only.
    3. Get the folder code from the shared link.
        - https://u.pcloud.link/publink/show?code=abcdefg
    4. Create a pCloud uploader account and use that username and password.
    5. Get folder ID by inspecting the network request when you upload a file in your browser.
        - https://api.pcloud.com/uploadfile?folderid=123456
    """
    print(tutorial_text)

def main():
    if len(sys.argv) <= 1:
        show_help()
        sys.exit(1)

    if sys.argv[1] == '--help':
        show_help()
        sys.exit(0)

    if sys.argv[1] == '--tutorial':
        show_pcloud_tutorial()
        sys.exit(0)

    if sys.argv[1] == '--setup':
        if len(sys.argv) != 6:
            print("    [Main] - Error. Invalid setup arguments. You need them all.")
            show_help()
            sys.exit(1)
        username = sys.argv[2]
        password = sys.argv[3]
        folder_id = sys.argv[4]
        folder_code = sys.argv[5]

        # Save credentials to constants.py
        with open(os.path.join(os.path.dirname(__file__), "constants.py"), "w") as f:
            f.write(f"# Auth\nusername = \"{username}\"\npassword = \"{password}\"\n\n# pCloud Folder\nfolder_id = \"{folder_id}\"\nfolder_code = \"{folder_code}\"")

        print("[Main] - Setup complete")
        sys.exit(0)

    if len(sys.argv) == 2:
        __verify_constants()
        url = sys.argv[1]
        download.download_audio(url)

        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio/")
        if not os.path.exists(folder):
            os.makedirs(folder)

        file_paths = os.listdir(folder)
        for file_name in file_paths:
            full_path = os.path.join(folder, file_name)
            upload.upload_file(file_name, full_path)
            os.remove(full_path)
            print(f"File {file_name} removed")

        print("[Main] - Exiting Successfully")
    else:
        show_help()
        sys.exit(1)

def __verify_constants():
    with open(os.path.join(os.path.dirname(__file__), "constants.py"), "r") as f:
        constants = f.read()
        if "username = " not in constants or "password = " not in constants or "folder_id = " not in constants or "folder_code = " not in constants:
            print("[Main] - Error. Constants are not set. Run --setup.")
            sys.exit(1)
    
    auth.get_active_auth_code()

if __name__ == '__main__':
    main()