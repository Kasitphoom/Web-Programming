import requests


def post_pram(name, surname, ID):
    url = "http://161.246.5.61:11328/students/newForm?student_name={}&student_surname={}&student_id={}".format(name, surname, ID)
    response = requests.post(url, json={"name": name, "surname": surname, "ID": ID})
    if response.status_code == 200:
        print(response.text)
    else:
        print("Error: ", response.status_code)

def post_link(name, surname, ID):
    url = "http://161.246.5.61:11328/students/new/{}/{}/{}/".format(name, surname, ID)
    response = requests.post(url)
    
    if response.status_code == 200:
        print(response.text)
    else:
        print("Error: ", response.status_code)
    
def post_json(name, surname, ID):
    url = "http://161.246.5.61:11328/students/new/"
    response = requests.post(url, json={"name": name, "surname": surname, "ID": ID})
    
    if response.status_code == 200:
        print(response.text)
    else:
        print("Error: ", response.status_code)

def get_html():
    url = "http://161.246.5.61:11328/students/html"
    response = requests.get(url)

    if response.status_code == 200:
        print(response.text)
    else:
        print("Error: ", response.status_code)

def get_html_id(ID):
    url = "http://161.246.5.61:11328/students/html/{}".format(ID)
    
    response = requests.get(url)

    if response.status_code == 200:
        print(response.text)
    else:
        print("Error: ", response.status_code)
        

post_pram("John", "Doe", 1234)
post_link("John", "Doe", 12345)
post_json("John", "Doe", 12346)

get_html()
get_html_id(1234)
get_html_id(12345)
get_html_id(12346)