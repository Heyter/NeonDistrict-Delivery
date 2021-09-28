import requests
import json
import pyNeonAccounts

def post(url, sid, data={}):
    response = requests.post("https://portal.neondistrict.io/" + url,
    data=json.dumps(data),
    headers={
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://portal.neondistrict.io",
        "Referer": "https://portal.neondistrict.io/neonpizza/delivery-agents",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    },
    cookies={"connect.sid": sid},
        auth=(),
    )

    return (response)


def login(username, password):
    print("======= " + username + " =======")

    response = requests.post('https://portal.neondistrict.io/api/account/login',
        headers={'Content-Type': 'application/json;charset=UTF-8'},
        data='{"email_or_username":"' + username + '","password":"' +
        password + '","remember_me":false,"code_2fa":""}'
    )

    if (response.status_code == 200):
        data = response.json()

        if (data["status"] == 200):
            cookie = response.cookies.get("connect.sid")
            response = post("api/neonpizza/bankTips", cookie)
            data = response.json()

            if (data["status"] == 200):
                print("bank-success", data)

                response = post("api/neonpizza/startShift", cookie, {"tier": pyNeonAccounts.TIER})
                data = response.json()

                if (data["status"] == 200):
                    print("delivery-success", data)
                else:
                    print("delivery-error", data)
            else:
                print("bank-error", data)
        else:
            print("response-error", data)

    print("==============================")
    print("")

if __name__ == "__main__":
    for keyAcc, valuePass in pyNeonAccounts.ACCOUNTS.items():
        login(keyAcc, valuePass)
