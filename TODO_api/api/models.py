from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TodoItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")
    title = models.CharField(max_length=100)
    content = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0)



    def __str__(self):
        return self.title
