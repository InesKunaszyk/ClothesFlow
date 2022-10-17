
import random
from django.contrib.auth import get_user_model, authenticate, login, logout

from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from .models import Donation, Institution

User = get_user_model()


class LandingPageView(View):
    template_name = 'user/index.html'

    def get(self, request, *args, **kwargs):
        bags_quantity = Donation.objects.aggregate(q=Sum('quantity'))
        bags = bags_quantity['q']
        organizations = Institution.objects.count()

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

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, form, *args, **kwargs):
        pass


class LoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'user/login.html')


class ConfirmationView(View):
    template_name = 'user/form-confirmation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
