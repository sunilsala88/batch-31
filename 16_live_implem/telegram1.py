



import requests
TOKEN = ''
ids = ''

message='this is my second message'
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ids}&parse_mode=Markdown&text={message}"
print(requests.get(url).json())