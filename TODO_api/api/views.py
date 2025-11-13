from django.shortcuts import render
from rest_framework import generics
from .models import TodoItem
from .serializers import TodoItemSerializer



class TodoItemListCreate(generics.ListCreateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer



class TodoItemRetrieveUptadeDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    lookup_field = 'pk'

