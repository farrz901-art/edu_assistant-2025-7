# # backend/apps/users/views.py
#
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import UserCreateSerializer
# from .models import User
# from django.contrib.auth import authenticate
# from rest_framework.permissions import AllowAny # <-- 新增导入
#
# class UserCreateView(APIView):
#     """
#     用户注册
#     """
#     permission_classes = [AllowAny] # <-- 新增行，允许任何用户访问
#     def post(self, request):
#         serializer = UserCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({
#                 "message": "User created successfully",
#                 "user": {
#                     "username": user.username,
#                     "role": user.role
#                 }
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class LoginView(APIView):
#     """
#     用户登录
#     """
#     permission_classes = [AllowAny] # <-- 新增行，允许任何用户访问
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             return Response({
#                 "message": "Login successful",
#                 "user": {
#                     "username": user.username,
#                     "role": user.role
#                 }
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#
