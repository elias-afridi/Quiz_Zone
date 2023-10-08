from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.db.models import Avg
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import *
from .models import *
# Create your views here.
def home(request,name=None):
    
    if name:
        quizes=Quiz.objects.filter(category=name)
   
    else:
        quizes=Quiz.objects.all()

    categories=Quiz.objects.all()
    
    context={'quizes':quizes,'categories':categories}
    return render(request,'Quiz/home.html',context)


def Register(request):
    if request.user.is_authenticated:
        return redirect('home') 
    
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
        


    return render(request,'Quiz/register.html',{'form':form})
    
def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        return render(request,'Quiz/login.html')

def Logout(request):
    logout(request)
    return redirect('login')

def AddQuestion(request):
    if request.user.is_staff:
        form=AddQuestionForm
        if(request.method=='POST'):
            form=AddQuestionForm(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('addQuestion')
        context={'form':form}
        return render(request,'Quiz/addQuestion.html',context)
    
    else:
        return redirect('home')
    
def AddQuiz(request):
    if request.user.is_staff:
        form=AddQuizForm
        if(request.method=='POST'):
            form=AddQuizForm(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('addQuiz')
        context={'form':form}
        return render(request,'Quiz/addQuiz.html',context)
    
    else:
        return redirect('home')
    
def TakeQuiz(request,quiz_id):
    if request.user.is_authenticated:

        quiz_instance=Quiz.objects.get(pk=quiz_id)
        if request.method == 'POST':
            print(request.POST)
            questions=Question.objects.filter(quiz=quiz_instance)
            score=0
            wrong=0
            correct=0
            total=0
            for q in questions:
                total+=1
                # print(request.POST.get(q.question))
                # print(q.answer)
                # print()
                # user_answer = request.POST.get(q.question)
                # print(f"Question: {q.question}")
                # print(f"Correct Answer: {q.answer}")
                # print(f"User's Answer: {user_answer}")
                # print()
                if q.answer ==  request.POST.get(q.question):
                    score+=q.mark
                    correct+=1
                else:
                    wrong+=1
            percent = score/(total*q.mark) *100
            context = {
                'score':score,
                'time': request.POST.get('timer'),
                'correct':correct,
                'wrong':wrong,
                'percent':percent,
                'total':total,
                'questions':questions
            }
            return render(request,'Quiz/result.html',context)
        else:
            questions=Question.objects.filter(quiz=quiz_instance)
            context = {
                'questions':questions,
                'quiz':quiz_instance
            }
            return render(request,'Quiz/takeQuiz.html',context)
    
    else:
        return redirect('register')
    

def RateQuiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            Rating.objects.update_or_create(user=request.user, quiz=quiz, defaults={'rating': rating})
            return redirect('quizDetail', quiz_id=quiz_id)
    else:
        form = RatingForm()
    
    return render(request, 'Quiz/rate.html', {'form': form, 'quiz': quiz})

def QuizDetail(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    average_rating = Rating.objects.filter(quiz=quiz).aggregate(Avg('rating'))['rating__avg']
    
    return render(request, 'Quiz/quizDetail.html', {'quiz': quiz, 'average_rating': average_rating})
