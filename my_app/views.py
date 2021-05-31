from django.shortcuts import render
from django.db import transaction
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import UserOTP, User
from twilio.rest import Client
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_encode_handler, jwt_get_secret_key
from rest_framework_jwt.utils import jwt_payload_handler
import jwt

# Create your views here.
class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            with transaction.atomic():
                data = request.data
                mobile_number = data.get('mobile_number')
                action = data.get('action')
                otp = request.data['otp']
                if action == 'GENERATE OTP':
                    user = User.objects.filter(mobile_number=mobile_number)
                    response = {"message":"User not found"}
                    if not user:
                        return Response(response, status=status.HTTP_404_NOT_FOUND)
                    key = UserOTP.objects.create(mobile_number=mobile_number, created_date=datetime.now())
                    key = key.key
                    account_sid = "AC241b7c980f8a729a310fc2bea054d704"
                    auth_token = "3ce930370a22e04f0c2496a212d5065d"
                    client = Client(account_sid, auth_token)
                    mobile_number = str(mobile_number)
                    country_code = "+91"
                    split_number = list(mobile_number)
                    if split_number[0] != "+":
                        mobile_number = country_code + mobile_number
                        print ("mm",mobile_number)
                    client.messages.create(
                        body=("You Otp for login is {}".format(key)),
                        from_='+15037136236',
                        to=mobile_number
                    )
                    response = {"message": "Check your registered mobile number for otp"}
                else:
                    user = User.objects.get(mobile_number=mobile_number)
                    otp_valid = UserOTP.objects.filter(mobile_number=mobile_number, key=otp).last()
                    if otp_valid and user:
                        try:
                            otp_valid.delete()
                            payload = jwt_payload_handler(user)
                            key = api_settings.JWT_PRIVATE_KEY or jwt_get_secret_key(payload)
                            token = jwt.encode(
                                payload,
                                key,
                                api_settings.JWT_ALGORITHM
                            )
                            user_details = {}
                            user_details['name'] = "%s %s" % (
                                user.first_name, user.last_name)
                            user_details['token'] = token
                            return Response(user_details, status=status.HTTP_200_OK)

                        except Exception as e:
                            raise e
                    else:
                        res = {
                            'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                        return Response(res, status=status.HTTP_403_FORBIDDEN)

                return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            response = {"message": "Something went wrong!"}
            return Response(response, status=status.HTTP_502_BAD_GATEWAY)