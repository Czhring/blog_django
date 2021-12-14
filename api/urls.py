from django.urls import path
from .views.users import SignUp

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign-up'),
]