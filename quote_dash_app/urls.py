from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('main_page', views.main_page),
    path('submit_quote', views.submit_quote),
    path('delete/<int:id>', views.delete_quote),
    path('like/<int:id>', views.add_like),
    path('user_account/<int:id>', views.user_account),
    path('edit/<int:id>', views.edit_user),
    path('user_quote/<int:id>', views.user_quote),
]