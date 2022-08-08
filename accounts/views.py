from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def g(request):
    ip_address = request.user.ip_address
    print(ip_address)
    return HttpResponse("hello")
