import json

import requests


# def send_otp(phone_number, code):
#     requests.get(
#         f"http://ws3584.isms.ir/sendWS?username=7bluesky&password=@7BS123456&mobiles[]={phone_number}&body= کد شما برای عضویت در سامانه{code}"
#     )

def send_otp(phone_number, code):
    headers = {"X-API-KEY": "EYzRJirmQWNEnkNUuY6X8XXiOZHCJVh5udl6RNUT3Wqpttuz4Pdjsv20p0KGFoax",
               "Content-Type": "application/json", "Accept": "*/*",
               }
    get_data = requests.post(
        url="https://api.sms.ir/v1/send/verify",
        headers=headers,
        data=json.dumps({
            "mobile": f"{phone_number}",
            "templateId": 100000,
            "parameters": [
                {
                    "name": "CODE",
                    "value": f"{code}"
                }
            ]
        },)

    )

    print(get_data.content)


