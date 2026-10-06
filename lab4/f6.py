import requests

def run():
    res = requests.get("https://httpbin.org/get")
    print("6. requests status code =", res.status_code)