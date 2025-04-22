

from django.urls import path
from .views import *


urlpatterns = [
    path('login_view/', post_list, name='post_list'),
    path('post_create/', post_create, name='post_create'),
    path('post_delete/<int:id>', post_delete, name='post_delete'),
    path('update_post/<int:id>', update_post, name='update_post'),
    path('register_view/',register_view,name='register'),
    path('',login_view,name='login_view'),
    path('logout/', logout_view, name='logout'),
    path('comment/<int:post_id>/', comment, name='comment'), 
    path('only/<int:id>/',only, name='only'),
    path('like/<int:post_id>/',toggle_like, name='toggle_like'),
    path('post/<int:id>/',only, name='only'),
     path('search/',search_view, name='search_view'), 
    
]

