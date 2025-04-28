from rest_framework.serializers import ModelSerializer
from .models import Bootcamp, BootcampCategory, BootcampRegistration
from rest_framework import serializers
from account.models import CustomUser


class BootCampCategorySerializer(ModelSerializer):
    class Meta:
        model = BootcampCategory
        fields = "__all__"



class BootCampSerializer(ModelSerializer):
    class Meta:
        model = Bootcamp
        fields = "__all__"        





class ListBootCampSerializer(ModelSerializer):
    class Meta:
        model = Bootcamp
        fields = ["title", "description", "start_date", "end_date", "is_online", "capacity", "price", "instructor", "category", "created_at", "hours", "days"]             





class RegisterBootCampSerializer(ModelSerializer):
    class Meta:
        model = BootcampRegistration
        fields = "__all__"
        read_only_fields = ('volunteer', 'status', 'slug', 'reviewed_by', 'reviewed_at', 'registered_at')


    def create(self, validated_data):
        validated_data["volunteer"] = self.context["request"].user
        return super().create(validated_data)
            

    


class AdminRegisterBootCampSerializer(ModelSerializer):
    class Meta:
        model = BootcampRegistration
        fields = "__all__"







class EditRegisterBootCampSerializer(ModelSerializer):
    class Meta:
        model = BootcampRegistration
        fields = "__all__"
        read_only_fields = ('volunteer', 'reviewed_by', 'reviewed_at', 'registered_at')
        


    def create(self, validated_data):
        validated_data["reviewed_by"] = self.context["request"].user
        return super().create(validated_data)
       






class RegistrationBootCampSerializer(ModelSerializer):
    
    class Meta:
        model = BootcampRegistration
        fields = ["bootcamp", "payment_type", "comment", "phone_number", "slug"]
        read_only_fields = ('reviewed_by', 'reviewed_at', 'registered_at', 'status', "volunteer")


    def create(self, validated_data):
          validated_data["volunteer"] = self.context["request"].user
          return super().create(validated_data)

    


