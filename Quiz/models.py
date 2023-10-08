from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Quiz(models.Model):
    title=models.CharField(max_length=100,unique=True)
    description=models.CharField(max_length=300,blank=True)
    category=models.CharField(max_length=100,unique=True)
    
    def __str__(self):
        return self.title
    
class Question(models.Model):
    quiz=models.ForeignKey(Quiz,related_name='quiz_question',on_delete=models.CASCADE)
    question=models.CharField(max_length=300,null=True)
    option_1=models.CharField(max_length=200,null=True)
    option_2=models.CharField(max_length=200,null=True)
    option_3=models.CharField(max_length=200,null=True)
    answer=models.CharField(max_length=200,null=True)
    mark=models.IntegerField(default=1)
    
    def __str__(self):
        return self.question
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),(6,'6'),(7,'7')])

    class Meta:
        unique_together = ['user', 'quiz']
