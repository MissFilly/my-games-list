from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView

from friendship.models import Friend

from mygameslist.app.mixins import LoginRequiredMixin
from .forms import FriendRequestForm


class FriendRequestView(FormView, LoginRequiredMixin):

    template_name = 'friends/request.html'
    form_class = FriendRequestForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.user2 = get_object_or_404(User, pk=kwargs['pk'])
        if self.request.user == self.user2:
            raise PermissionDenied()
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
