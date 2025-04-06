from django.urls import path
from . import views
import kagglehub

model_path = kagglehub.model_download("qadeer884/emplyee-chrun-prediction/scikitLearn/default")

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('predict/', views.predict_view, name='predict'),
    path('complete/<int:task_id>/', views.task_complete, name='task_complete'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),
]
