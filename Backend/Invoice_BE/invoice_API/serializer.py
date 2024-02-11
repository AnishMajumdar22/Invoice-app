from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data["name"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("name", "password")

    def validate(self, data):
        user = authenticate(**data)
        # print("Received credentials", user)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemList
        exclude = ("invoice",)


class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemListSerializer(many=True, read_only=True)  # items coming from models.py

    class Meta:
        model = Invoice
        fields = "__all__"
