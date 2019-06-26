
from django.shortcuts import render

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q, Avg, Count
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from braces import views

from analytics.models import TagView
from .models import Tag



class TagDetailView(DetailView):
    model=Tag

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            tag = self.get_object()

            new_view = TagView.objects.add_count(self.request.user, tag)
        return context




class TagListView(ListView):
    model=Tag
    def get_queryset(self, *args, **kwargs):
        usun_zbedne_tagi()
        qs = Tag.objects.filter(active=True)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                ).order_by("title")
        return qs


def usun_zbedne_tagi():
    for t in Tag.objects.all():
        if t.products.all().count() == 0:
            t.delete()
    return Tag.objects.all()
