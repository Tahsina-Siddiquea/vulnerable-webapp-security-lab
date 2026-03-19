import requests
from report_generator import generate_report


TARGET = "http://localhost:5000"


def test_sqli():
    print("\n========================================")
    print("SQL Injection Test")
    print("========================================")

    payload = "admin'--"

    data = {
        "username": payload,
        "password": "anything"
    }

    try:
        r = requests.post(f"{TARGET}/login", data=data)

        if "Welcome admin" in r.text or r.status_code == 302:
            print("Payload:", payload)
            print("Result: Authentication bypassed")
            return {"exploited": True, "fixed": False}
        else:
            print("Payload:", payload)
            print("Result: Attack blocked")
            return {"exploited": False, "fixed": True}

    except Exception as e:
        print("Error:", e)
        return {"exploited": False, "fixed": False}


def test_xss():
    print("\n========================================")
    print("XSS Test")
    print("========================================")

    payload = "<script>alert('XSS')</script>"

    try:
        r = requests.get(f"{TARGET}/search?q={payload}")

        if payload in r.text:
            print("Payload:", payload)
            print("Result: Script executed in browser")
            return {"exploited": True, "fixed": False}
        else:
            print("Payload:", payload)
            print("Result: Attack blocked")
            return {"exploited": False, "fixed": True}

    except Exception as e:
        print("Error:", e)
        return {"exploited": False, "fixed": False}


def test_idor():
    print("\n========================================")
    print("IDOR Test")
    print("========================================")

    try:
        r = requests.get(f"{TARGET}/user/2/profile")

        if "bob" in r.text.lower() or r.status_code == 200:
            print("Accessed: /user/2/profile")
            print("Result: Private profile accessed")
            return {"exploited": True, "fixed": False}
        else:
            print("Accessed: /user/2/profile")
            print("Result: Access denied")
            return {"exploited": False, "fixed": True}

    except Exception as e:
        print("Error:", e)
        return {"exploited": False, "fixed": False}


def test_csrf():
    print("\n========================================")
    print("CSRF Test")
    print("========================================")

    data = {
        "email": "attacker@evil.com"
    }

    try:
        r = requests.post(f"{TARGET}/contact", data=data)

        if r.status_code == 200:
            print("Forged request sent")
            print("Result: Email changed")
            return {"exploited": True, "fixed": False}
        else:
            print("Forged request blocked")
            return {"exploited": False, "fixed": True}

    except Exception as e:
        print("Error:", e)
        return {"exploited": False, "fixed": False}


def main():

    print("\n========================================")
    print("Running Web Security Lab Scanner")
    print("Target:", TARGET)
    print("========================================")

    results = {}

    results["sqli"] = test_sqli()
    results["xss"] = test_xss()
    results["idor"] = test_idor()
    results["csrf"] = test_csrf()

    print("\n========================================")
    print("Generating dynamic security report...")
    print("========================================")

    generate_report(results, TARGET)


if __name__ == "__main__":
    main()