"""
Views for the user API
"""
from rest_framework import generics
from user.serializer import UserSerializer
from django.shortcuts import render

class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    """
    serializer_class = UserSerializer


