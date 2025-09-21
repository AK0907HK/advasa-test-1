from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db import transaction
from .models import Application, UserProfile

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    initial_allowance = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ("username", "password", "initial_allowance")

    def validate_initial_allowance(self, v):
        if v is None:
            return v
        if not isinstance(v, int) or v < 1:
            raise serializers.ValidationError("1以上の整数を入力してください")
        return v

    def create(self, validated_data):
        initial = validated_data.pop("initial_allowance", None)
        username = validated_data["username"]
        password = validated_data["password"]

        user = User(username=username)
        user.set_password(password)
        user.save()  

        if initial is not None:
            prof = user.profile
            prof.available_amount = initial
            prof.save(update_fields=["available_amount"])

        return user

class ApplicationCreateSerializer(serializers.ModelSerializer):
    
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = Application
        fields = ("id", "amount", "status", "created_at")
        read_only_fields = ("id", "status", "created_at")

    def create(self, validated_data):
        user = self.context["request"].user
        amount = validated_data["amount"]

        with transaction.atomic():
            profile = UserProfile.objects.select_for_update().get(user=user)

            if profile.available_amount < amount:
                raise serializers.ValidationError({"amount": ["申請可能額を超えています"]})

            profile.available_amount -= amount
            profile.save(update_fields=["available_amount"])

            app = Application.objects.create(user=user, amount=amount)

        return app

class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "amount", "status", "created_at")        