from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # 任意。指定があれば残高に反映（1以上の整数のみ）
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
        user.save()  # signals で profile が自動生成される

        if initial is not None:
            prof = user.profile
            prof.available_amount = initial
            prof.save(update_fields=["available_amount"])

        return user
