import requests

headers = {
    "Authorization": "Api-Key wkll0ikz.xMinHyPa45FZOwRTHeqXF60cv7Z0yv8S"
}

r = requests.get("http://127.0.0.1:8000/todos/", headers=headers)
print(r.json())
