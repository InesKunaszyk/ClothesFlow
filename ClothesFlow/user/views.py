
import random
from django.contrib.auth import get_user_model, authenticate, login, logout

from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import View, FormView

from .models import Donation, Institution

User = get_user_model()


class LandingPageView(View):
    template_name = 'user/index.html'

    def get(self, request, *args, **kwargs):
        bags_quantity = Donation.objects.aggregate(q=Sum('quantity'))
        bags = bags_quantity['q']
        organizations_amount = Donation.objects.aggregate(n=Count('institution', distinct=True))
        organizations = organizations_amount['n']

        foundation = Institution.objects.filter(type='1')
        organization = Institution.objects.filter(type='2')
        local_collection = Institution.objects.filter(type='3')

        return render(request, self.template_name, {'bags': bags,
                                                    'organizations': organizations,
                                                    'f': foundation,
                                                    'o': organization,
                                                    'lc': local_collection,
                                                    })


class AddDonationView(View):
    template_name = 'user/form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RegisterView(View):
    template_name = 'user/register.html'
    # success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if email is None:
            raise ValueError('Email jest niezbędny do rejestracji. Podaj email.')

        if password != password2:
            raise ValueError('Hasła musza być takie same!')

        user = User.objects.create_user(
            first_name=name,
            last_name=surname,
            email=email,
            password=password,
        )
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return render(request, 'user/login.html')


class LoginView(View):
    template_name = 'user/login.html'
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, ):
        pass


class ConfirmationView(View):
    template_name = 'user/form-confirmation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
