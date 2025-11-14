from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path('todos/public/', views.TodoItemListCreatePublic.as_view(), name='todo-public-view-create'),
    path('todos/', views.TodoItemListCreate.as_view(), name='todo-view-create'),
    path('todos/<int:pk>/', views.TodoItemRetrieveUptadeDestroy.as_view(), name='todo-detail'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
