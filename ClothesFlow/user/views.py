import json
import random
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured

from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import View, CreateView, FormView, UpdateView

from .forms import UserCreateForm, UserLoginForm, UserProfileForm

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

    def post(self, request, *args, **kwargs):
        summary = request.POST
        print(summary)

        return JsonResponse(summary)
        # donation = Donation(quantity=data['bag'],
        #                     categories=data['categories'],
        #                     institution=data['institution'],
        #                     address=data['address'],
        #                     phone_number=data[''])_
        # donation.save()

        # return JsonResponse({'quantity': item.quantity, 'name': item.name})

    #     print(request.body)
    #     form = request.body
    #     filename = 0
    #     for ff in form:
    #         filename += 1
    #         with open(f"{filename}.jpg", "wb+") as f:
    #             f.write(ff)
    #     return JsonResponse(status=201)
    #     # data = json.loads(request.body)
        # response = []
        # print(response)
        # return JsonResponse({'response': response})


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
        cd = form.cleaned_data
        email = cd.get("email")
        password = cd.get("password")
        if email not in User.objects.filter(email=email):
            return redirect('register')
        # else:


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class ConfirmationView(View):
    template_name = 'user/form-confirmation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserProfileView(LoginRequiredMixin, CreateView):
    template_name = 'user/user_profile.html'
    model = User
    form_class = UserProfileForm


class UserUpdateProfileView(UserPassesTestMixin, UpdateView):
    template_name = 'user/user_update_profile.html'
    model = User
    form_class = UserProfileForm

    def test_func(self):
        # Prevents editing other profiles
        return self.request.user.is_authenticated and self.request.user.pk == self.kwargs["pk"]

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_pk = kwargs.get("pk")
            user = User.objects.get(pk=user_pk)

            cd = form.cleaned_data
            first_name = cd.get('name')
            last_name = cd.get('surname')
            email = cd.get('email')
            password = cd.get('password')
            user = authenticate(password=password)

            if user.is_authenticated:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                return redirect('login')


            # else:
            #     return render(request, "user/user_update_profile.html", {"message": "Wprowadzone hasło jest błędne!"})

        # valid_password = request.user.check_password(password)
        # if user.is_authenticated and valid_password:


        # user = User.objects.get(pk=request.user.id)
        # first_name = request.POST['name']
        # last_name = request.POST['surname']
        # email = request.POST['email']
        # valid_password = request.user.check_password(request.POST['password'])
        #
        # if valid_password:
        #     user.first_name = first_name
        #     user.last_name = last_name
        #     user.email = email
        #     user.save()
        #
        #     return redirect('login')
        #
        # return render(
        #     request,
        #     'user_update_profile.html',
        #     context={
        #         'message': "Wprowadzone hasło jest niepoprawne!"
        #     })