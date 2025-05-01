from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from account.models import CustomUser




class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__al__"
        read_only_fields = ["is_paid"]




class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()


    class Meta:
        model = CustomUser
        fields = ["email", "ful_name", "date_created"]


    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"     
    



class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def validate(self, attrs):
        method = attrs.get("method")
        tracking_code = attrs.get("tracking_code")
        receipt_image = attrs.get("receipt_image")

        if method == "offline":
            if not tracking_code:
                raise serializers.ValidationError("tracking_code can not be empty!")
            if not receipt_image:
                raise serializers.ValidationError("receipt_image must be uploaded!")
        return attrs    
        



class PaymentListSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
       