from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField






class CreateStudentSerializer(serializers.ModelSerializer):
    group = serializers.CharField(write_only=True, required=False)  

    class Meta:
        model = CustomUser
        fields = [
            "username", "first_name", "last_name", "phone", "email",
            "about_me", "national_id", "gender", "group"
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["phone"] = str(instance.phone)
        return representation

    def create(self, validated_data):
        group_name = validated_data.pop('group', None)  

        user = CustomUser.objects.create(**validated_data)

        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                raise serializers.ValidationError(f"Group '{group_name}' does not exist.")

        user.set_unusable_password()
        user.save()
        return user



class OTPSerializer(serializers.Serializer):
    phone = PhoneNumberField(unique=True,region="IR")