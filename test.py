from urllib import response
import requests

BASE = "http://localhost:5000/"

response = requests.get(BASE + "todo")
print(response.json())

data = [{"title": "Laudnry", "description": "Do the laundry"},
        {"title": "Gaming", "description": "Go gaming"}]

input()
for i in range(len(data)):
    response = requests.post(BASE + "todo", data[i])
    print(response.json())

input()
response = requests.get(BASE + "todo/0")
print(response.json())

input()
requests.put(BASE + "todo/0", {"title": "Eat dinner", "description": "Eat dinner after doing the laundry."})
print(response.json())

response = requests.get(BASE + "todo/0")
print(response.json())

input()
response = requests.put(BASE + "todo/0/finish")
print(response.json())

response = requests.get(BASE + "todo/0")
print(response.json())

input()
response = requests.delete(BASE + "todo/0")
print(response)

response = requests.get(BASE + "todo/0")
print(response.json())