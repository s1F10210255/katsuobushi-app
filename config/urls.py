"""config URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from team import views as team_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', team_views.index, name='index'),
    path('announce', team_views.announce, name='announce'),
    path('clear', team_views.clear, name='clear'),
    path('api/echo', team_views.echo, name='api_echo'),
    path('api/hello', team_views.hello, name='api_hello'),
    path('api/reply', team_views.reply, name='api_reply'),
    path('api/katsuobushi',team_views.katsuobushi, name='api_katsuobushi'),



]