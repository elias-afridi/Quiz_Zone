from django.urls import path
from .views import home,AddQuestion,AddQuiz,TakeQuiz,Register,Login,Logout,RateQuiz,QuizDetail
urlpatterns = [
    path('',home,name='home'),
    path('register/',Register,name='register'),
    path('login/',Login,name='login'),
    path('logout/',Logout,name='logout'),
    path('addQueston/',AddQuestion,name='addQuestion'),
    path('addQuiz/',AddQuiz,name='addQuiz'),
    path('category/<str:name>/',home,name='quiz_by_category'),
    path('takeQuiz',TakeQuiz,name='takeQuiz'),
    path('takeQuiz/<int:quiz_id>',TakeQuiz,name='selectedQuiz'),
    path('rateQuiz/<int:quiz_id>/', RateQuiz, name='rateQuiz'),
    path('quizDetail/<int:quiz_id>/', QuizDetail, name='quizDetail'),
]
