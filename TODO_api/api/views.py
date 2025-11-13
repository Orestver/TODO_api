from django.shortcuts import render
from rest_framework import generics, status, filters, permissions
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer



class TodoItemListCreate(generics.ListCreateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

    filter_backends = [filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['priority','title', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return TodoItem.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    # Override delete method 
    def delete(self, request, *args, **kwargs):
        TodoItem.objects.filter(owner=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class TodoItemRetrieveUptadeDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    lookup_field = 'pk'


    def get_queryset(self):
        return TodoItem.objects.filter(owner=self.request.user)

