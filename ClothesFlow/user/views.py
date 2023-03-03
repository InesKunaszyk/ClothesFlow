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
from django.utils import timezone

from django.views.generic import View, CreateView, FormView, UpdateView, ListView

from .forms import UserCreateForm, UserLoginForm, UserProfileForm, NewDonationForm

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


class AddDonationView(LoginRequiredMixin, FormView):
    template_name = 'user/form.html'
    login_url = 'login'
    permission_denied_message = 'Aby przekazać dary musisz być zalogowany.'
    form_class = NewDonationForm
    success_url = reverse_lazy("conf")

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        organizations = Institution.objects.all()

        return render(request, self.template_name, {'categories': categories,
                                                    'organizations': organizations,
                                                    })

    def post(self, request, *args, **kwargs):
        data = request.POST
        chosen_categories = request.POST.getlist("categories")
        chosen_institution = data["institution"]
        institution = Institution.objects.get(pk=chosen_institution)
        donation_categories = Category.objects.filter(pk__in=chosen_categories)

        new_donation = Donation.objects.create(
            quantity=data["bag"],
            address=data["address"],
            phone_number=data["phone_number"],
            city=data["city"],
            zip_code=data["zip_code"],
            pick_up_date=data["date"],
            pick_up_time=data["time"],
            pick_up_comment=data["more_info"],
            institution=institution,
            user=request.user,
        )

        new_donation.categories.set(donation_categories)
        new_donation.save()

        return render(request, 'user/form-confirmation.html')


class DonationConfirmationView(View):

    def get(self, request):
        return render(request, 'user/form-confirmation.html')


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
        return redirect('landing_page')

    def form_invalid(self, form):
        message = "Podano błędne dane. Spróbuj ponownie"
        return HttpResponse(message)


class UserLogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'user/user_profile.html'
    model = User
    form_class = UserProfileForm

    def get_queryset(self):
        return Donation.objects.filter(user_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.request.user.id)
        return context


# class ArchiveDonationView(CreateView):
#
#     def post(self, request, *args, **kwargs):
#         user_pk = kwargs['pk']
#         picked_up_donation = request.user.donation_set.get(pk=user_pk)
#         print(user_pk)
#         print(picked_up_donation)
#
#         # walidacja
#         if "confirmation" in request.POST:
#             picked_up_donation.is_taken = True
#             picked_up_donation.taken_time = timezone.now()
#             picked_up_donation.save()
#
#
#         if "cancel_confirmation" in request.POST:
#             picked_up_donation.is_taken = False
#             picked_up_donation.taken_time = None
#             picked_up_donation.save()
#
#         return redirect('profile', user_pk)
