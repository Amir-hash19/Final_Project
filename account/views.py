from rest_framework.generics import CreateAPIView, ListAPIView
from .permissions import GroupPermission
from .models import CustomUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CreateStudentSerializer, OTPSerializer, VerifyOTPSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .tasks import send_otp_task
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from rest_framework.throttling import AnonRateThrottle
from .OTPthrottling import OTPThrottle
from django.contrib.auth import get_user_model






class RegisterAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateStudentSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
                },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class SendOTPView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [OTPThrottle]
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = str(serializer.validated_data["phone"])

            send_otp_task.delay(phone) 


            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








MAX_FAILED_ATTEMPTS = 5
BLOCK_TIME_SECONDS = 300  # 5 دقیقه

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = str(serializer.validated_data["phone"])
            otp = serializer.validated_data["otp"]

            fail_key = f"otp_fail:{phone}"
            blocked = cache.get(fail_key)

            if blocked and int(blocked) >= MAX_FAILED_ATTEMPTS:
                return Response({"error": "Too many attempts. Please try again later."},
                                status=status.HTTP_429_TOO_MANY_REQUESTS)

            cached_otp = cache.get(f"otp:{phone}")
            if cached_otp and str(cached_otp) == otp:
                cache.delete(f"otp:{phone}")  # پاک کردن OTP موفق
                cache.delete(fail_key)  # پاک کردن شمارنده تلاش ناموفق

                # ✅ ساخت JWT token
                user = get_user_model().objects.filter(phone=phone).first()
                if not user:
                    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                })

            else:
                # افزایش شمارنده تلاش ناموفق
                current_fails = cache.get(fail_key, 0)
                cache.set(fail_key, int(current_fails) + 1, timeout=BLOCK_TIME_SECONDS)

                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    






