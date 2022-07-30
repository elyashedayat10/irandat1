from random import randint

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from ..models import OtpCode
from ..utils import send_otp
from .serializers import (LoginSerializer, PasswordChangeSerializer,
                          PasswordResetSerializer,
                          PasswordResetVerifiedSerializer, PhoneSerializer,
                          VerifySerializer, UserSerializer)

user = get_user_model()


class SendOtpApiView(GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data["phone_number"]
            password = serializer.validated_data['password']
            random_number = randint(111111, 999999)
            try:
                user_obj = user.objects.create_user(phone_number=phone_number, password=password)
                user_obj.is_active = False
                user_obj.save()
                OtpCode.objects.create(
                    phone_number=phone_number, code=random_number
                )
                send_otp(phone_number, random_number)
                return Response(data={
                    "message": "code sent",
                }, status=status.HTTP_200_OK)
            except Exception:
                return Response(data={
                    "message": "user  already exists",
                }, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyApiView(GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data["phone_number"]
            code = serializer.validated_data["code"]
            otp_obj = OtpCode.objects.filter(phone_number=phone_number).last()
            if otp_obj and otp_obj.code == str(code):
                user_obj = user.objects.get(phone_number=phone_number)
                user_obj.is_active = True
                user_obj.save()
                token, create = Token.objects.get_or_create(user_id=user_obj.id)
                context = {
                    "message": "کاربر با موفقیت وارد شد",
                    "data": token.key,
                }
                return Response(data=context, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': "رمز وارد شده درست نمیباشذ"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message": serializer.errors}, status=status.HTTP_502_BAD_GATEWAY)


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_obj = authenticate(request, phone_number=serializer.validated_data['phone_number'],
                                    password=serializer.validated_data['password'])
            if user_obj is not None and user.is_active:
                token, create = Token.objects.get_or_create(user_id=user_obj.id)
                context = {
                    "message": "user login in successfully",
                    "data": token.key,
                }
                return Response(data=context, status=status.HTTP_200_OK)
            return Response(data={'message': 'user dose not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        """
        Remove all auth tokens owned by request.user.
        """
        tokens = Token.objects.filter(user=request.user)
        for token in tokens:
            token.delete()
        content = {'success': 'User logged out.'}
        return Response(content, status=status.HTTP_200_OK)


class PasswordChange(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            new_password = serializer.data['new_password']
            old_password = serializer.data['old_password']

            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            content = {'detail': 'your old password is not valid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.data['phone_number']

            try:
                user_obj = user.objects.get(phone_number=phone_number)
                random_number = randint(111111, 999999)
                send_otp(user_obj.phone_number, random_number)
                content = {'success': 'send email.'}
                return Response(content, status=status.HTTP_200_OK)

            except user.DoesNotExist:
                content = {'error': 'Email dose not exists..'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerify(GenericAPIView):
    serializer_class = PasswordResetVerifiedSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.data['phone_number']
            new_password = serializer.data['new_password']

            try:
                user_obj = user.objects.get(phone_number=phone_number)
                user_obj.set_password(new_password)
                user_obj.save()
                content = {'success': 'verify password.'}
                return Response(content, status=status.HTTP_200_OK)

            except user.DoesNotExist:
                content = {'error': 'Wrong/Expired Token!.'}
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminListApiView(ListAPIView):
    queryset = user.objects.filter(is_admin=True)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]


class AdminCreateApiView(CreateAPIView):
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    def perform_create(self, serializer):
        serializer.save(is_admin=True)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'new admin created',
            'data': response.data
        })


class AdminDeleteApiView(DestroyAPIView):
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            'message': 'admin deleted',
        })
