from rest_framework.serializers import ModelSerializer
from .models import CustomUser




class CreateStudentSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "phone", "email", "about_me", "national_id", "gender"]



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["phone"] = str(instance.phone)
        return representation
    
    


    
       
