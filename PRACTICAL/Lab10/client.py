import requests

url = "http://161.246.5.61:11328/students/html"
url2 = "http://161.246.5.61:11328/students/123456"


response = requests.post("http://161.246.5.61:11328/students/newForm?student_name=John&student_surname=Smith&student_id=1234")
if response.status_code == 200:
    print(response.text)
else:
    print("Error: ", response.status_code)
    
response = requests.post("http://161.246.5.61:11328/students/new/abc/abc/12345")
if response.status_code == 200:
    print(response.text)
else:
    print("Error: ", response.status_code)
    
response = requests.post("http://161.246.5.61:11328/students/new/", json={"name": "John", "surname": "Smith", "ID": "123456"})
if response.status_code == 200:
    print(response.text)
else:
    print("Error: ", response.status_code)



response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print("Error: ", response.status_code)
    
response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print("Error: ", response.status_code)