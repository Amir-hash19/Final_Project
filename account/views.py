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
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = str(serializer.validated_data["phone"])

            send_otp_task.delay(phone) 


            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class VerifyOTPView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = str(serializer.validated_data["phone"])
            otp = serializer.validated_data['otp']

            cached_otp = cache.get(f"otp:{phone}")

            if cached_otp is None:
                return Response({"detail": "OTP expired or not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            if str(cached_otp) != str(otp):
                return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
            

            user, created = CustomUser.objects.get_or_create(phone=phone, defaults={"username": phone})


            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh":str(refresh),
                "access":str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    






