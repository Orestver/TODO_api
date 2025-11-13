from django.db import models

# Create your models here.

class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
