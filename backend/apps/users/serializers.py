# from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from .models import User
#
#
#
# class UserCreateSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'role']
#
#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)  # 使用 set_password 方法加密密码
#         user.save()
#         return user
#
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['role'] = user.role
#         return token
