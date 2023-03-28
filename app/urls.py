from django.urls import path
from app.views import *
app_name="app"
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path("<int:pk>/",DetailView.as_view(),name="detail"),
    path('<int:pk>/results',ResultView.as_view(), name="results"),
    path('<int:id>/vote/',vote, name="vote"),
]
