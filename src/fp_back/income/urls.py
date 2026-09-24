from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.add),
    path('delete/', views.delete),
    # path('edit/', views.edit),
    # path('copy/', views.copy),
    # path('upload/', views.upload),
    # path('download/', views.download),
]
'''
Каждая функция может быть реализована так что принимать на вход
сущность, поля для неё и обрабатывать в соответствии.
'''
