from django.urls import path

from accounts.views import RegisterView, LoginView, logoutuser, UserView, UserEditView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logoutuser),
    path('profile/view/', UserView.as_view()),
    path('profile/edit/', UserEditView.as_view())
]