from django.db.models import Sum, Count
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from .models import Donation, Institution


class LandingPageView(View):
    template_name = 'user/index.html'

    def get(self, request, *args, **kwargs):
        bags_quantity = Donation.objects.aggregate(q=Sum('quantity'))
        bags = bags_quantity['q']
        organizations = Institution.objects.count()

        return render(request, self.template_name, {'bags': bags, 'organizations': organizations})


class AddDonationView(View):
    template_name = 'user/form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RegisterView(View):
    template_name = 'user/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'user/login.html')


class ConfirmationView(View):
    template_name = 'user/form-confirmation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)