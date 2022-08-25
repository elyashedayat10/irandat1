from random import randint

from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from config.models import Notification

from ..models import OtpCode
from ..utils import send_otp
from .permissions import IsSuperUser
from .serializers import (
    AdminSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    PasswordResetVerifiedSerializer,
    PhoneSerializer,
    UserMainSerializers,
    UserSerializer,
    VerifySerializer,
    UpdateUserSerializers,
)

user = get_user_model()


class SendOtpApiView(GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data["phone_number"]
            first_name = serializer.validated_data["first_name"]
            last_name = serializer.validated_data["last_name"]
            password = serializer.validated_data["password"]
            random_number = randint(111111, 999999)
            user_obj = user.objects.filter(phone_number=phone_number).first()
            if not user_obj:
                user_obj = user.objects.create_user(
                    phone_number=phone_number,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                user_obj.is_active = False
                user_obj.save()
                OtpCode.objects.create(phone_number=phone_number, code=random_number)
                send_otp(phone_number, random_number)
                return Response(
                    data={
                        "message": "code sent",
                    },
                    status=status.HTTP_200_OK,
                )
            elif user_obj and user_obj.is_active:
                return Response(
                    data={
                        "message": "user  already exists",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                OtpCode.objects.create(phone_number=phone_number, code=random_number)
                send_otp(phone_number, random_number)
                return Response(
                    data={
                        "message": "code resend to user",
                    },
                    status=status.HTTP_200_OK,
                )

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
                Notification.objects.create(
                    text=f"{phone_number} به تازگی در برنامه عضو شده "
                )
                return Response(data=context, status=status.HTTP_200_OK)
            else:
                return Response(
                    data={"message": "رمز وارد شده درست نمیباشذ"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_obj = authenticate(
                request,
                phone_number=serializer.validated_data["phone_number"],
                password=serializer.validated_data["password"],
            )
            if user_obj is not None and user.is_active:
                token, create = Token.objects.get_or_create(user_id=user_obj.id)
                context = {
                    "message": "user login in successfully",
                    "data": token.key,
                    "admin": True if user_obj.is_admin else False,
                }
                return Response(data=context, status=status.HTTP_200_OK)
            return Response(
                data={"message": "user dose not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, format=None):
        """
        Remove all auth tokens owned by request.user.
        """
        tokens = Token.objects.filter(user=request.user)
        for token in tokens:
            token.delete()
        content = {"success": "User logged out."}
        return Response(content, status=status.HTTP_200_OK)


class PasswordChange(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            new_password = serializer.data["new_password"]
            old_password = serializer.data["old_password"]

            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            content = {"detail": "your old password is not valid"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.data["phone_number"]
            try:
                user_obj = user.objects.get(phone_number=phone_number)
                random_number = randint(111111, 999999)
                OtpCode.objects.create(phone_number=phone_number, code=random_number)
                send_otp(user_obj.phone_number, random_number)
                content = {"success": "otp sent."}
                return Response(content, status=status.HTTP_200_OK)
            except user.DoesNotExist:
                content = {"error": "phone_number dose not exist.."}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerify(GenericAPIView):
    serializer_class = PasswordResetVerifiedSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.data["phone_number"]
            new_password = serializer.data["new_password"]
            code = serializer.data["code"]
            otp_obj = OtpCode.objects.filter(phone_number=phone_number).last()
            if otp_obj and otp_obj.code == str(code):
                try:
                    user_obj = user.objects.get(phone_number=phone_number)
                    user_obj.set_password(new_password)
                    user_obj.save()
                    content = {"success": "verify password."}
                    return Response(content, status=status.HTTP_200_OK)
                except user.DoesNotExist:
                    content = {"error": "user dose not exist!."}
                    return Response(data=content, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {"error": "Wrong/code!."}
                return Response(data=content, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminListApiView(ListAPIView):
    queryset = user.objects.filter(is_admin=True)
    serializer_class = AdminSerializer
    permission_classes = [
        IsAdminUser,
    ]


class AdminCreateApiView(CreateAPIView):
    queryset = user.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def perform_create(self, serializer):
        serializer.save(is_admin=True)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "new admin created", "data": response.data})


class AdminDeleteApiView(DestroyAPIView):
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response(
            {
                "message": "admin deleted",
            }
        )


class UserListApiView(ListAPIView):
    queryset = user.objects.exclude(is_admin=True, is_superuser=True)
    serializer_class = UserMainSerializers
    permission_classes = [
        IsAdminUser,
    ]


class MakeAdminUserApiView(GenericAPIView):
    serializer_class = UserMainSerializers
    permission_classes = [
        IsSuperUser,
    ]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        user_obj = get_object_or_404(user, pk=pk)
        user_obj.is_admin = True
        user_obj.save()
        return Response(
            {"message": "user upgrade to admin user"}, status=status.HTTP_200_OK
        )


class MakeNormalUserApiView(GenericAPIView):
    serializer_class = UserMainSerializers
    permission_classes = [
        IsSuperUser,
    ]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        user_obj = get_object_or_404(user, pk=pk)
        user_obj.is_admin = False
        user_obj.save()
        return Response(
            {"message": "user dowmgraded to normal user"}, status=status.HTTP_200_OK
        )


class UpdateUserApiView(UpdateAPIView):
    serializer_class = UpdateUserSerializers
    queryset = user.objects.all()

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(
            data={
                "status": 200,
                "message": "user updated",
            }
        )
