from rest_framework.generics import CreateAPIView, ListAPIView
from .permissions import GroupPermission
from .models import CustomUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CreateStudentSerializer






class RegisterAccountView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CreateStudentSerializer

  


