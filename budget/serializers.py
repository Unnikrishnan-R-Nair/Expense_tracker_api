from rest_framework import serializers

from django.contrib.auth.models import User

from budget.models import Expense, Income


class UserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True)

    password2 = serializers.CharField(write_only=True)

    class Meta:

        model = User

        fields = ["id", "username", "email", "password", "password1", "password2"]

        read_only_fields = ["id", "password"]

    
    def create(self, validated_data):

        print(validated_data)

        password1 = validated_data.pop("password1")

        password2 = validated_data.pop("password2")

        if password1 != password2:

            raise serializers.ValidationError("Passwords mismatch. Try again!!!")

        return User.objects.create_user(**validated_data, password=password1)


class ExpenseSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()

    class Meta:

        model = Expense

        fields = "__all__"

        read_only_fields = ["id", "owner", "created_date"]


class IncomeSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()

    class Meta:

        model = Income

        fields = "__all__"

        read_only_fields = ["id", "owner", "created_date"]

