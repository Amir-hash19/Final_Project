from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveUpdateAPIView
from .permissions import GroupPermission
from .models import CustomUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CreateAccountSerializer, OTPSerializer, VerifyOTPSerializer, CreateSupportAdminSerializer, DeleteAccountSerializer, DetailsAccountSerializer, ListSupportPanelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .tasks import send_otp_task, send_welcome_sms_task
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from rest_framework.throttling import AnonRateThrottle
from .OTPthrottling import OTPThrottle
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination



class CustomPagination(PageNumberPagination):
    page_size = 20



@method_decorator(csrf_exempt, name='dispatch')
class RegisterAccountView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
          
            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
                },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class SendOTPLogInView(APIView):
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
BLOCK_TIME_SECONDS = 300  

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
                cache.delete(f"otp:{phone}")  
                cache.delete(fail_key)  

             
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
    
    



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Token deleted successfully"})






class CreateSupportAdminView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = CreateSupportAdminSerializer





#سوپریوز میتونه اکانت بقیه رو پاک کنه 
class DeleteSupportAdminView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser")]
    serializer_class = DeleteAccountSerializer

    def perform_destroy(self, instance):
        if self.request.user == instance:
            raise ValidationError("You Cannot delete own account from here")
        instance.delete()
        






class DeleteAccount(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteAccountSerializer

    def get_object(self):
        return self.request.user
        
    


#برای کاربر عادی هستش
class AccountDetailsView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DetailsAccountSerializer
    
    def get_object(self):
        return self.request.user
        






class ListSupportAccountView(ListAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated,GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = ListSupportPanelSerializer
    pagination_class = CustomPagination