from random import randint

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..models import OtpCode
from ..utils import send_otp
from .serializers import PhoneSerializer, VerifySerializer

user = get_user_model()


class SendOtpApiView(GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data["phone_number"]
            random_number = randint(111111, 999999)
            OtpCode.objects.create(
                phone_number=phone_number, code=random_number
            )
            send_otp(phone_number, random_number)
            return Response(data={
                "message": "کد برای کاربر ارسال شد",
            }, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyApiView(GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data["phone_number"]
            code = serializer.validated_data["code"]
            fcm_token = serializer.validated_data['fcm_token']
            otp_obj = OtpCode.objects.filter(phone_number=phone_number).last()
            if otp_obj and otp_obj.code == str(code):
                try:
                    user_obj = user.objects.get(phone_number=phone_number)
                    token, create = Token.objects.get_or_create(user_id=user_obj.id)
                    context = {
                        "message": "کاربر با موفقیت وارد شد",
                        "data": token.key,
                    }
                    return Response(data=context, status=status.HTTP_200_OK)
                except:
                    user_obj = user.objects.create_user(phone_number=phone_number, fcm_token=fcm_token)
                    token = Token.objects.create(user=user_obj)
                    context = {
                        "message": "کاربر با موفقیت ساخته شد",
                        "data": token.key,
                    }
                    return Response(data=context, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': "رمز وارد شده درست نمیباشذ"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message": serializer.errors}, status=status.HTTP_502_BAD_GATEWAY)


class LoginApiView(GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        if serializer.is_valid(raise_exception=True):
            user_obj = authenticate(request, phone_number=serializer.validated_data['phone_number'],
                                    password=serializer.validated_data['password'])
            if user is not None:
                token, create = Token.objects.get_or_create(user_id=user_obj.id)
                context = {
                    "message": "کاربر با موفقیت ساخته شد",
                    "data": token.key,
                }
                return Response(data=context, status=status.HTTP_200_OK)
            return Response(data={'message': 'کاربر با مسخصان وارد شدع وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
