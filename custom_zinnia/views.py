from django.db.models import Q
from django.utils import timezone
from zinnia.managers import PUBLISHED
from zinnia.models.entry import Entry
from django.views.generic import TemplateView, DetailView, ListView


class Blog(ListView):
    model = Entry
    paginate_by = 12
    template_name = 'stocks/blogs.html'
    context_object_name = 'blogs'
    queryset = Entry.objects.filter(
                    Q(start_publication__isnull=True) | Q(start_publication__lt=timezone.now()),
                    Q(end_publication__isnull=True) | Q(end_publication__gt=timezone.now()),
                    status=PUBLISHED
                ).only('title', 'lead', 'slug', 'image', 'image_caption', 'authors', 'publication_date')


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
