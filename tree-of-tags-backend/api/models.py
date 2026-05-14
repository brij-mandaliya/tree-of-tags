from django.db import models

# Create your models here.

class Tree(models.Model):
    json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tree"

    def __str__(self):
        return f"Tree {self.id}"
