from django.shortcuts import render
from rest_framework import generics, status, filters, permissions
from rest_framework.response import Response
from .models import TodoItem, UserAPIKey
from .serializers import TodoItemSerializer
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey
from .forms import RegisterForm
from rest_framework_api_key.permissions import HasAPIKey
from django.contrib.auth import authenticate, login

permission_classes = [HasAPIKey]


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            if User.objects.filter(username=username).exists():
                return render(request, "registration.html", {"form": form, "error": "Користувач з таким логіном вже існує."})
            user = User.objects.create_user(username=username, password=password)

            api_key_obj, plain_key = APIKey.objects.create_key(name=f"{username}_key")

            # зберігаємо копію plaintext ключа у своїй моделі
            UserAPIKey.objects.create(user=user, key=plain_key)

            # (опціонально) автоматично логінемо користувача
            login(request, user)
            

            return render(request, "success.html", {"api_key": plain_key, "message": "Користувача створено."})
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                user_key_obj = user.api_key_copy 
                saved_key = user_key_obj.key
            except UserAPIKey.DoesNotExist:
                # Якщо ключа немає — створимо новий і збережемо
                api_key_obj, plain_key = APIKey.objects.create_key(name=f"{username}_key")
                saved_key = plain_key
                UserAPIKey.objects.create(user=user, key=plain_key)
            

            return render(request, "success.html", {"api_key": saved_key, "message": "Log in successful."})

        return render(request, "login.html", {"error": "Invalid login or password."})

    return render(request, "login.html")
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
    

class TodoItemListCreatePublic(generics.ListCreateAPIView):

    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

    filter_backends = [filters.OrderingFilter]
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

