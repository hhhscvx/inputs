from django.urls import path
from . import views


urlpatterns = [
    path('contact-with-us/', views.ContactWithUs.as_view(), name='contact_with_us')
]
