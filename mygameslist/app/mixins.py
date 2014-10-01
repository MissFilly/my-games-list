from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import ListEntry


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class EntryMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        self.entry = get_object_or_404(ListEntry, game_id=kwargs['pk'],
                                       user=request.user)
        return super(EntryMixin, self).dispatch(request, *args,
                                                **kwargs)


class PermissionMixin(LoginRequiredMixin, SingleObjectMixin):

    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        if obj.user:
            owner = obj.user
        elif obj.entry:
            owner = obj.entry.user
        elif obj.entry1:
            owner = obj.entry1.user

        if not owner == self.request.user:
            raise HttpResponseForbidden
        else:
            return obj
