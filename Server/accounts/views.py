from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseNotAllowed, Http404, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import FormView
from accounts.forms import RegisterForm, EditUserForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                 last_name=last_name)
        return HttpResponseRedirect('/accounts/login/')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if user := authenticate(username=username, password=password):
            login(request, user)
            return HttpResponseRedirect('/accounts/profile/view/')
        else:
            error = 'Username or password is invalid'
            return TemplateResponse(request, 'accounts/login.html',
                                    context={'errors': [error]})


def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        # return TemplateResponse(request, 'accounts/login.html')
        return HttpResponseRedirect('/accounts/login/')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


class UserView(View):

    def get(self, request, *args, **kwargs):
        # print("FINDING USER")
        # print("USER AUTHENTICATED: ", self.request.user.is_authenticated)

        if not self.request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        # print("USER:", self.request.user)
        u = User.objects.get(username=self.request.user)
        # branch = Branch.objects.get(id=self.kwargs['branch_id'])
        # print(branch.name)
        user = get_object_or_404(User, username=self.request.user)
        # print("USER", user.username)
        data = {'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,

                }
        return JsonResponse(data)


class UserEditView(FormView):
    template_name = 'accounts/edituser.html'
    form_class = EditUserForm

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponse('Unauthorized User', status=401)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("BACKEND AUTH!!!")
        if not self.request.user.is_authenticated:
            return HttpResponse('Unauthorized User', status=401)

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.request.user)
        # print("EDITING USER: ", user)
        context = super(UserEditView, self).get_context_data(**kwargs)
        context['user'] = user
        return context

    def form_valid(self, form):
        # print("UPDATING USER...")
        # name = form.cleaned_data['name']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        email = form.cleaned_data['email']
        # conso
        # if password1 == '':
            # print("EMPTY PASSWORD")
        # print("GETTING USER")
        # print("FORM USER: ", form.user)
        u = get_object_or_404(User, username=self.request.user)
        # print("OLD PASS: ", u.password)

        u.first_name, u.last_name, u.email = \
            first_name, last_name, email
        u.save()
        if password1 != '':
            u.set_password(password1)
            u.save()
            # print("EMPTY PASSWORD")
        # if user := authenticate(username=u.username, password=u.password):
        #     login(self.request, user)
        #     return HttpResponseRedirect('/accounts/profile/view')
        # print("NEW PASS: ", u.password)
        # print('AUTH ', u.is_authenticated)
        update_session_auth_hash(self.request, u)
        # print("UPDATED USER: ", u.id, u.username, u.is_authenticated)
        return HttpResponseRedirect('/accounts/profile/view/')
