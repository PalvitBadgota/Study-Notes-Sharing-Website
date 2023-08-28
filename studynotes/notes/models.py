from django.db import models
from django.contrib.auth.models import User


class signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    branch = models.CharField(max_length=30)
    role = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploading_date = models.CharField(max_length=30, null=True)
    branch = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    notes_file = models.FileField()
    filetype = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=15, default="pending")

    def __str__(self):
        return self.user.username+" "+self.status
