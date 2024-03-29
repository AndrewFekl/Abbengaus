from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('translate', views.TranslateView.as_view(), name='translate'),
    path('train', views.TrainingView.as_view(), name='train'),
]
