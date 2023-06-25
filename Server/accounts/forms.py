from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def clean(self):
        data = super().clean()
        password1 = data.get('password1', '')
        # if len(data.get('username', '')) < 6:
        #     self.add_error("username", "Username must be at least 6 characters")
        if len(password1) < 8:
            self.add_error("password1", "This password is too short. It must contain at least 8 characters")

        username = data.get('username', '')
        if User.objects.filter(username=username).exists():
            self.add_error("username", "A user with that username already exists")


        password2 = data.get('password2', '')
        email = data.get('email', '')

        if email != '':
            try:
                validate_email(email)
            except ValidationError:
                self.add_error("email", "Enter a valid email addressa")
        if password1 != password2:
            print(password1, password2, 'NOT MATCH')
            self.add_error("password1", "The two password fields didn't match")

        return data


class EditUserForm(forms.Form):
    # username = forms.CharField(max_length=100)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password1 = forms.CharField(max_length=100, required=False)
    password2 = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)

    def clean(self):
        # print("CLEANING FORM")
        data = super().clean()

        # if len(data.get('password1', '')) < 8:
        #     self.add_error("password1", "This password is too short. It must contain at least 8 characters")
        #
        password1 = data.get('password1', '')
        if password1 != '' and len(password1) < 8:
            self.add_error("password1", "This password is too short. It must contain at least 8 characters")

        password2 = data.get('password2', '')
        # email = data.get('email', '')
        #
        # try:
        #     validate_email(email)
        # except ValidationError:
        #     self.add_error("email", "Enter a valid email address")
        if password1 != password2:
            self.add_error("password1", "The two password fields didn't match")
        # print("END CLEANING")
        return data
