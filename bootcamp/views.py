from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from .models import BootcampCategory, Bootcamp, BootcampRegistration
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from account.permissions import GroupPermission
from .serializers import( BootCampCategorySerializer, BootCampSerializer, ListBootCampSerializer, 
RegisterBootCampSerializer, AdminRegisterBootCampSerializer, EditRegisterBootCampSerializer, RegistrationBootCampSerializer)
from account.views import CustomPagination




#ساختن دسته بندی توسط ادمین ها
class CreateBootCampCategoryView(CreateAPIView):
    queryset = BootcampCategory.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootCampCategorySerializer





#ساختن بوتکمپ توسط سوپر یوزر و پنل ادمین
class CreateBootCampView(CreateAPIView):
    queryset = Bootcamp.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootCampSerializer



#پاک کردن دسته بندی توسط پنل ادمین و سوپریوزر
class DeleteBootCampCategoryView(DestroyAPIView):
    queryset = BootcampCategory.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootCampCategorySerializer
    



#پاک کردن بوت کمپ توسط پنل ادمین و سوپریوزر
class DeleteBootCampView(DestroyAPIView):
    queryset = Bootcamp.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootCampSerializer






class ListBootcampView(ListAPIView):
    queryset = Bootcamp.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootCampSerializer
    pagination_class = CustomPagination






class ListBootCampCategoryView(ListAPIView):
    queryset = BootcampCategory.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootCampCategorySerializer
    pagination_class = CustomPagination







class UpdateBootCampView(UpdateAPIView):
    queryset = Bootcamp.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootCampSerializer



#ازاد برای همه 
class ListAvailableBootCamp(ListAPIView):
    queryset = Bootcamp.objects.filter(status="registering")
    permission_classes = [AllowAny]
    serializer_class = ListBootCampSerializer
    pagination_class = CustomPagination




#ازاد برای همه 
class CreateRegisterBootCampView(CreateAPIView):
    queryset = BootcampRegistration.objects.all()# یه سیگنال برای این بنویس 
    permission_classes = [IsAuthenticated]
    serializer_class = RegistrationBootCampSerializer





#فقط برای درخواست های بررسی نشده هستش این ویو 
class ListRegisterBootCampView(ListAPIView):
    queryset = BootcampRegistration.objects.filter(status="pending")
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel")]
    serializer_class = AdminRegisterBootCampSerializer
    pagination_class = CustomPagination





class EditRegisterBootCampView(UpdateAPIView):
    queryset = BootcampRegistration.objects.filter(status="pending")
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel")]
    serializer_class = EditRegisterBootCampSerializer#درسته






