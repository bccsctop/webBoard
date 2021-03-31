from django.db import models
from django.contrib.auth.models import User

class Topic (models.Model):
    topicid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=150)
    like = models.IntegerField()
    userid = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment (models.Model):
    commentid = models.AutoField(primary_key=True)
    content = models.CharField(max_length=150)
    like = models.IntegerField()
    comuserid = models.ForeignKey(User, on_delete=models.CASCADE)
    comtopicid = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Create (models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    topicid = models.ForeignKey(Topic, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.date

class Write (models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    commentid = models.ForeignKey(Comment, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.date

class Tag (models.Model):
    topicid = models.ForeignKey(Topic, on_delete=models.CASCADE)
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag