from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import LoginRawForm, SignUpForm


class LoginFormView(FormView):
    form_class = LoginRawForm
    success_url = reverse_lazy('index')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = authenticate(self.request,
                            username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password'))

        if user:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        return HttpResponseRedirect(reverse_lazy('login'))


class SignUpFormView(CreateView):
    form_class = SignUpForm
    success_url = '/'
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])

        return super().form_valid(form)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/index.html'
