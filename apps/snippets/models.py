from email.policy import default
from django.db import models
# Create your models here.

#Model to create Objects in Database
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True, default="")
    highscore = models.IntegerField(blank=True, null=True, default=0)
    
    
    class Meta:
        ordering = ['created']
        
  