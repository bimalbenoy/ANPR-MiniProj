
from django.urls import path
from .  import views
urlpatterns = [
    path('register/', views.registerveh, name='registerveh'),
    path('contact/', views.contact, name='contact'),
    path('registerlogbook/', views.registerlogbook, name='registerlogbook'),
    path('animatedregister/', views.animatedregister, name='animatedregister'),
    path('register/', views.register, name='register'),  # Note: duplicate route
    path('home1/', views.home1, name='home1'),
    path('logbook/', views.logbook, name='logbook'),
    path('upload/', views.upload, name='upload'),
    path('gateopen/', views.gateopen, name='gateopen'),
    path('gateclose/', views.gateclose, name='gateclose'),
    path('criminalgateclose/', views.criminalgateclose, name='criminalgateclose'),
]
