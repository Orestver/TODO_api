from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.TodoItemListCreate.as_view(), name='todo-view-create'),
    path('todos/<int:pk>/', views.TodoItemRetrieveUptadeDestroy.as_view(), name='todo-detail')
]
