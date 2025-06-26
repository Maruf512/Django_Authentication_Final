from django.db import models



class Account(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.email
