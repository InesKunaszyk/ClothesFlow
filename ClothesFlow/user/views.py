from django.shortcuts import render

# Create your views here.
from django.views.generic import View


class LandingPageView(View):
    template_name = 'user/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AddDonationView(View):
    template_name = 'user/form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RegisterView(View):
    template_name = 'user/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginView(View):

    def get(self, request):
        return render (request, 'user/login.html')