from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

class CustomUserRateThrottle(UserRateThrottle):
    rate= '10/day'


