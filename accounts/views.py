from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def g(request):
    ip_address = request.user.ip_address
    print(ip_address)
    return HttpResponse("hello")
