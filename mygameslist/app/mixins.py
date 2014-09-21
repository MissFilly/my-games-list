from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import ListEntry


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class EntryMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        self.entry = get_object_or_404(ListEntry, game__pk=kwargs['pk'],
                                       user=request.user)
        return super(EntryMixin, self).dispatch(request, *args,
                                                **kwargs)
