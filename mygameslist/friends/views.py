from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from friendship.models import Friend, FriendshipRequest

from mygameslist.app.mixins import LoginRequiredMixin, PermissionMixin
from .forms import FriendRequestForm


class FriendRequestView(FormView, LoginRequiredMixin):

    template_name = 'friends/request.html'
    form_class = FriendRequestForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.user2 = get_object_or_404(User, pk=kwargs['pk'])
        if self.request.user == self.user2:
            raise PermissionDenied()
        elif FriendshipRequest.objects.filter(from_user=self.request.user,
                                              to_user=self.user2).exists():
            return HttpResponse(_('You already sent a request to this user.'))
        return super(FriendRequestView, self).dispatch(request,
                                                       *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        message_relationship = Friend.objects.add_friend(
            from_user=self.request.user,
            to_user=self.user2,
            message=form.cleaned_data.get('message'),
        )
        return super(FriendRequestView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(FriendRequestView, self).get_context_data(**kwargs)
        context['user_requested'] = self.user2
        return context


class ReceivedRequestsView(LoginRequiredMixin, ListView):
    model = FriendshipRequest
    template_name = 'friends/requests.html'

    def get_queryset(self):
        return FriendshipRequest.objects.filter(to_user=self.request.user)


class FriendshipRequestAction(PermissionMixin, SingleObjectMixin, View):
    model = FriendshipRequest

    def post(self, request, *args, **kwargs):
        action = kwargs.get('action')
        friend_request = self.get_object()

        if action == 'accept':
            friend_request.accept()
        else:
            friend_request.mark_viewed()
            if action == 'reject':
                friend_request.reject()

        return redirect(reverse('friends_list'))


class FriendListView(TemplateView, LoginRequiredMixin):
    template_name = 'friends/friends_list.html'
