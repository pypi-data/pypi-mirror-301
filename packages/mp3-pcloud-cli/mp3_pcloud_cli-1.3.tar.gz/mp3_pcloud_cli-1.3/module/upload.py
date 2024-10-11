import requests
from . import auth, constants

def upload_file(fileName, filePath):
    auth_code = auth.get_active_auth_code()    
    url = f"https://api.pcloud.com/publink/upload?auth={auth_code}&folderid={constants.folder_id}&code={constants.folder_code}"    

    response = requests.request("POST", url, files=[('',(fileName ,open(filePath,'rb'),''))])    
    
    if (response.json().get("result") == 0):
        print("[Upload] - File uploaded successfully")
    else:
        print("[Upload] - Error uploading file. Response: ", response.text)
        return Exception("[Upload] Error uploading file")