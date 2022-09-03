import json
import requests
from celery import shared_task


@shared_task(ignore_result=True)
def send_otp(phone_number, code):
    headers = {
        "X-API-KEY": "EYzRJirmQWNEnkNUuY6X8XXiOZHCJVh5udl6RNUT3Wqpttuz4Pdjsv20p0KGFoax",
        "Content-Type": "application/json",
        "Accept": "*/*",
    }
    requests.post(
        url="https://api.sms.ir/v1/send/verify",
        headers=headers,
        data=json.dumps(
            {
                "mobile": f"{phone_number}",
                "templateId": 100000,
                "parameters": [{"name": "CODE", "value": f"{code}"}],
            },
        ),
    )
