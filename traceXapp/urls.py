"""traceXapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from traceXDev.views import render_index, registration_page, user_login_submit, admin_page, \
    admin_add_commute_page, admin_view_all_commutes_page, admin_search_commutes_page, add_commute, get_all_commute_data, \
    mark_commute_action, register_user, user_home_page, get_user_commute_data, user_view_all_commutes, \
    user_subscribe_commute

urlpatterns = [
    path('', render_index),
    path('registration_page', registration_page),
    path('user_login_submit', user_login_submit),
    path('register_user', register_user),
    path('admin_page', admin_page),
    path('user_home_page', user_home_page),
    path('login_page', render_index),
    path('admin_add_commute_page', admin_add_commute_page),
    path('admin_view_all_commutes_page', admin_view_all_commutes_page),
    path('add_commute', add_commute),
    path('get_all_commute_data', get_all_commute_data),
    path('mark_commute_action', mark_commute_action),
    path('get_user_commute_data', get_user_commute_data),
    path('user_view_all_commutes', user_view_all_commutes),
    path('user_subscribe_commute', user_subscribe_commute),
    path('admin_search_commutes_page', admin_search_commutes_page),

    path('admin/', admin.site.urls),
]
