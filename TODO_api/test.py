import requests

url = "http://127.0.0.1:8000/todos/"
response = requests.get(url)
data = response.json()
print(response.status_code)
print(response.json())
for item in data:
    print("Title:", item['title'])
    print("Content:", item['content'])
