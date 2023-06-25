from django.urls import path

from banks.views import RegisterBankView, BanksView, BankDetails, BranchDetailsView, RegisterBranchView, BranchEditView

# from accounts.views import RegisterView, LoginView, logoutuser, UserView

urlpatterns = [
    path('add/', RegisterBankView.as_view()),
    path('<int:bank_id>/details/', BankDetails.as_view()),
    path('all/', BanksView.as_view()),
    path('<int:bank_id>/branches/add/', RegisterBranchView.as_view()),
    path('branch/<int:branch_id>/details/', BranchDetailsView.as_view()),
    path('branch/<int:branch_id>/edit/', BranchEditView.as_view())
]