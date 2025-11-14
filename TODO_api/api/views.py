from django.shortcuts import render
from rest_framework import generics, status, filters, permissions
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey
from .forms import RegisterForm
from rest_framework_api_key.permissions import HasAPIKey

permission_classes = [HasAPIKey]


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']


            user = User.objects.create_user(username=username, password=password)

            api_key, key = APIKey.objects.create_key(name=f'{username}_key')

            return render(request, "success.html", {"api_key": key})
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {"form": form})



class TodoItemListCreate(generics.ListCreateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

    filter_backends = [filters.OrderingFilter]
    permission_classes = [HasAPIKey]
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

