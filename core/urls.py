from django.urls import path
from core import views

urlpatterns = [
    path('', views.HighScores.as_view(), name='high-scores'),
    path('new-game', views.NewGameView.as_view()),
    path(
        'question/<str:game>/<int:question>',
        views.QuestionView.as_view(),
        name='question',
    ),
    path('answer/<str:game>/<int:question>', views.AnswerView.as_view(), name='answer'),
    path('results/<str:game>', views.ResultView.as_view(), name='results'),
]
