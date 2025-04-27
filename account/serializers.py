from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import ModelSerializer






class CreateAccountSerializer(serializers.ModelSerializer):
    group = serializers.CharField(write_only=True, required=False)
   

    class Meta:
        model = CustomUser
        fields = [
            "username", "first_name", "last_name", "phone", "email",
            "about_me", "national_id", "gender","group",
        ]
        read_only_fields = ['group']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["phone"] = str(instance.phone) 
        return data

    def create(self, validated_data):
        group_name = validated_data.pop('group', None)

        user = CustomUser.objects.create(**validated_data)

        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                raise serializers.ValidationError(f"Group '{group_name}' does not exist.")

        user.save()
        return user







class OTPSerializer(serializers.Serializer):
    phone = PhoneNumberField(region="IR")
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['phone'] = str(instance.phone)
        return representation
    






class VerifyOTPSerializer(serializers.Serializer):
    phone = PhoneNumberField(region="IR")
    otp = serializers.CharField(max_length=6)
    




class CreateSupportAdminSerializer(serializers.ModelSerializer):
    group = serializers.CharField(default="SupportPanel", required=False)  

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        group_name = validated_data.pop('group', 'SupportPanel')  
        user = CustomUser.objects.create(**validated_data)

        try:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group) 
        except Exception as e:
            raise serializers.ValidationError(f"Error adding group: {str(e)}")  

        # ذخیره کردن کاربر
        user.save()

        return user
    



class DeleteAccountSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"    




class DetailsAccountSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"



class ListSupportPanelSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"