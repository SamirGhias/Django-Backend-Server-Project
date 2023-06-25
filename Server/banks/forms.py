from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



class RegisterBankForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=100, required=True)
    inst_num = forms.CharField(max_length=100, required=True)
    swift_code = forms.CharField(max_length=100, required=True)

    # owner = models.ForeignKey(to=User, null=True, on_delete=SET_NULL)

    def clean(self):
        data = super().clean()

        name = data.get('name', '')
        if len(name) > 100:
            self.add_error("name", f"Ensure this value has at most 100 characters (it has <{len(name)}>)")

        description = data.get('description', '')
        if len(description) > 100:
            self.add_error("description", f"Ensure this value has at most 100 characters (it has <{len(description)}>)")

        inst_num = data.get('inst_num', '')
        if len(inst_num) > 100:
            self.add_error("inst_num", f"Ensure this value has at most 100 characters (it has <{len(inst_num)}>)")

        swift_code = data.get('swift_code', '')
        if len(swift_code) > 100:
            self.add_error("swift_code", f"Ensure this value has at most 100 characters (it has <{len(swift_code)}>)")


        return data


class RegisterBranchForm(forms.Form):
    name = forms.CharField(max_length=100)
    transit_num = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    email = forms.CharField()
    capacity = forms.IntegerField(min_value=0, required=False)

    # owner = models.ForeignKey(to=User, null=True, on_delete=SET_NULL)

    def clean(self):
        data = super().clean()
        name = data.get('name', '')
        if len(name) > 100:
            self.add_error("name", f"Ensure this value has at most 100 characters (it has <{len(name)}>)")

        transit_num = data.get('transit_num', '')
        if len(transit_num) > 100:
            self.add_error("transit_num", f"Ensure this value has at most 100 characters (it has <{len(transit_num)}>)")

        address = data.get('address', '')
        if len(address) > 100:
            self.add_error("address", f"Ensure this value has at most 100 characters (it has <{len(address)}>)")

        email = data.get('email', '')

        try:
            validate_email(email)
        except ValidationError:
            self.add_error("email", "Enter a valid email address")
        # if password != password2:
        #     self.add_error("password", "The two password fields didn't match")

        return data


class EditBranchForm(forms.Form):
    name = forms.CharField(max_length=100)
    transit_num = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    email = forms.CharField()
    capacity = forms.IntegerField(min_value=0, required=False)

    # owner = models.ForeignKey(to=User, null=True, on_delete=SET_NULL)

    def clean(self):
        data = super().clean()
        data = super().clean()
        name = data.get('name', '')
        if len(name) > 100:
            self.add_error("name", f"Ensure this value has at most 100 characters (it has <{len(name)}>)")

        transit_num = data.get('transit_num', '')
        if len(transit_num) > 100:
            self.add_error("transit_num", f"Ensure this value has at most 100 characters (it has <{len(transit_num)}>)")

        address = data.get('address', '')
        if len(address) > 100:
            self.add_error("address", f"Ensure this value has at most 100 characters (it has <{len(address)}>)")

        email = data.get('email', '')

        try:
            validate_email(email)
        except ValidationError:
            self.add_error("email", "Enter a valid email address")
        # if password != password2:
        #     self.add_error("password", "The two password fields didn't match")

        return data
