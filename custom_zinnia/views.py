from django.db.models import Q
from django.utils import timezone
from zinnia.managers import PUBLISHED
from zinnia.models.entry import Entry
from django.views.generic import TemplateView, DetailView


class Blog(TemplateView):
    template_name = 'stocks/blogs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        now = timezone.now()
        all_blogs = Entry.objects.filter(
            Q(start_publication__isnull=True) | Q(start_publication__lt=now),
            Q(end_publication__isnull=True) | Q(end_publication__gt=now),
            status=PUBLISHED
        ).only('title', 'lead', 'slug', 'image')
        context = {'data': all_blogs}
        return context


class BlogDetail(DetailView):
    template_name = 'stocks/BlogDetail.html'
    model = Entry

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        now = timezone.now()

        selected_blog = Entry.objects.filter(
            Q(start_publication__isnull=True) | Q(start_publication__lt=now),
            Q(end_publication__isnull=True) | Q(end_publication__gt=now),
            status=PUBLISHED
        ).get(slug=self.kwargs['slug'])

        context = {'data': selected_blog}

        return context
