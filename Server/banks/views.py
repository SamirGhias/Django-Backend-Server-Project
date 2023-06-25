from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import FormView

import banks.models
from banks.forms import RegisterBankForm, EditBranchForm, RegisterBranchForm
from banks.models import Bank, Branch
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class RegisterBankView(FormView):
    template_name = 'banks/createbank.html'
    form_class = RegisterBankForm

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        # u = User.objects.get(username=self.request.user)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        inst_num = form.cleaned_data['inst_num']
        swift_code = form.cleaned_data['swift_code']
        # print(description)
        if not self.request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        u = User.objects.get(username=self.request.user)
        b = Bank.objects.create(name=name,
                            description=description,
                            inst_num=inst_num,
                            swift_code=swift_code,
                            owner=u)
        return HttpResponseRedirect('/banks/'+ str(b.id)  +'/details/')


class BankDetails(View):
    def get(self, request, *args, **kwargs):
        # banks = Bank.objects.all()
        # bank = Bank.objects.get(id=request.)

        print(self.kwargs['bank_id'])

        try:
            Bank.objects.get(id=self.kwargs['bank_id'])
        except ObjectDoesNotExist:
            return HttpResponse('404 ERROR NOT FOUND', status=404)

        bank = Bank.objects.get(id=self.kwargs['bank_id'])
        # print(bank.name)
        branches = Branch.objects.filter(bank=bank)
        # print(branches)
        return TemplateResponse(request, 'banks/bankdetails.html', context={'bank': bank, 'branches': branches})


class BanksView(View):
    def get(self, request, *args, **kwargs):
        banks = Bank.objects.all()
        # print(banks)
        return TemplateResponse(request, 'banks/allbanks.html', context={'banks': banks})


class RegisterBranchView(FormView):
    template_name = 'banks/createbranch.html'
    form_class = RegisterBranchForm

    #
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        u = User.objects.get(username=self.request.user)
        try:
            print("AUTHING")
            b = Bank.objects.get(id=self.kwargs['bank_id'])
            print(b.owner)
            print(u)
            if b.owner != u:
                print(b.owner)
                print(u)
                print("NOT OWNER")
                return HttpResponse('FORBIDDEN', status=403)
        except ObjectDoesNotExist:
            return HttpResponse('NOT FOUND', status=404)

        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):

        bank = Bank.objects.get(id=self.kwargs['bank_id'])
        print("REGISTERING BRANCH FOR", bank)
        context = super(RegisterBranchView, self).get_context_data(**kwargs)
        context['bank'] = bank
        return context

    def form_valid(self, form):
        print("CREATING BRANCH...")
        name = form.cleaned_data['name']
        transit_num = form.cleaned_data['transit_num']
        address = form.cleaned_data['address']
        email = form.cleaned_data['email']
        capacity = form.cleaned_data['capacity']
        # print(self.kwargs)


        if not self.request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        u = User.objects.get(username=self.request.user)
        try:
            print("AUTHING again")
            b = Bank.objects.get(id=self.kwargs['bank_id'])
            print(b.owner)
            print(u)
            if b.owner != u:
                print(b.owner)
                print(u)
                print("NOT OWNER")
                return HttpResponse('FORBIDDEN', status=403)
        except ObjectDoesNotExist:
            return HttpResponse('NOT FOUND', status=404)


        bank = Bank.objects.get(id=self.kwargs['bank_id'])
        print(bank)
        # u = User.objects.get(username=self.request.user)
        br = Branch.objects.create(name=name,
                                   transit_num=transit_num,
                                   address=address,
                                   email=email,
                                   capacity=capacity,
                                   bank=bank)
        print("CREATED BRANCH: ", br.id, br.last_modified)
        return HttpResponseRedirect(f'/banks/branch/{br.id}/details/')


class BranchDetailsView(View):

    def get(self, request, *args, **kwargs):
        # print("FINDING BRANCH")
        if not self.request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        # branch = Branch.objects.get(id=self.kwargs['branch_id'])
        # print(branch.name)
        br = get_object_or_404(Branch, id=self.kwargs['branch_id'])
        # print("OBJ", br.name)
        data = {'id': br.id,
                'name': br.name,
                'transit_num': br.transit_num,
                'address': br.address,
                'email': br.email,
                'capacity': br.capacity,
                'last_modified': br.last_modified
                }
        return JsonResponse(data)


class BranchEditView(FormView):
    template_name = 'banks/editbranch.html'
    form_class = EditBranchForm

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponse('Unauthorized User', status=401)
        u = User.objects.get(username=self.request.user)

        br = get_object_or_404(Branch, id=self.kwargs['branch_id'])

        b = Bank.objects.get(id=br.bank.id)

        if b.owner != u:
            # print("NOT OWNER")
            return HttpResponse('FORBIDDEN', status=403)
        # print("HES THE OWNER")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("BACKEND AUTH!!!")
        if not self.request.user.is_authenticated:
            return HttpResponse('Unauthorized User', status=401)
        u = User.objects.get(username=self.request.user)

        br = get_object_or_404(Branch, id=self.kwargs['branch_id'])

        b = Bank.objects.get(id=br.bank.id)

        if b.owner != u:
            # print("NOT OWNER")
            return HttpResponse('FORBIDDEN', status=403)

        return super().post(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        branch = Branch.objects.get(id=self.kwargs['branch_id'])
        # print("EDITING BRANCH: ", branch)
        context = super(BranchEditView, self).get_context_data(**kwargs)
        context['branch'] = branch
        return context

    def form_valid(self, form):
        # print("UPDATING BRANCH...")
        name = form.cleaned_data['name']
        transit_num = form.cleaned_data['transit_num']
        address = form.cleaned_data['address']
        email = form.cleaned_data['email']
        capacity = form.cleaned_data['capacity']
        # print(self.kwargs)

        b = get_object_or_404(Branch, id=self.kwargs['branch_id'])
        b.name, b.transit_num, b.address, b.email, b.capacity = \
            name, transit_num, address, email, capacity
        b.save()
        # print("UPDATED BRANCH: ", b.id, b.last_modified)
        return HttpResponseRedirect(f'/banks/branch/{b.id}/details/')
