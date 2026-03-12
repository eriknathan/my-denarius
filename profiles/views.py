from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, View

from .forms import ProfileForm, UserUpdateForm
from .models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'profiles/form.html'
    success_url = reverse_lazy('profiles:detail')

    def get_object(self):
        return self.request.user.profile

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        profile_form = ProfileForm(instance=profile)
        user_form = UserUpdateForm(instance=request.user)
        return self._render(request, profile_form, user_form)

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        profile_form = ProfileForm(request.POST, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Perfil atualizado com sucesso.')
            return HttpResponseRedirect(self.success_url)
        return self._render(request, profile_form, user_form)

    def _render(self, request, profile_form, user_form):
        from django.shortcuts import render
        return render(request, self.template_name, {
            'form': profile_form,
            'user_form': user_form,
        })
