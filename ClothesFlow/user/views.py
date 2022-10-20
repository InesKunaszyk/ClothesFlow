
import random
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured

from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import View, CreateView, FormView

from .forms import UserCreateForm, UserLoginForm

from .models import Donation, Institution, Category

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


class AddDonationView(LoginRequiredMixin, View):
    template_name = 'user/form.html'
    login_url = 'login'
    permission_denied_message = 'Aby przekazać dary musisz być zalogowany.'
    redirect_field_name = 'add_donation'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        organizations = Institution.objects.all()

        return render(request, self.template_name, {'categories': categories,
                                                    'organizations': organizations,
                                                    })


class RegisterView(FormView):
    form_class = UserCreateForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        cd = form.cleaned_data
        first_name = cd.get('name')
        last_name = cd.get('surname')
        email = cd.get('email')
        password = cd.get('password')
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('landing_page')

    def form_valid(self, form):
        cd = form.cleaned_data
        email = cd.get("email")
        password = cd.get("password")
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('register')


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class ConfirmationView(View):
    template_name = 'user/form-confirmation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
