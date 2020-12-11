
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name = "home"),
    path('analysis', views.analysis, name='analysis'),
    path('reunion', views.reunion, name='reunion'),
]
