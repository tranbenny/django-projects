from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from blog.models import Post

# PREVIOUS VERSION OF POST LIST REQUEST HANDLER
# def post_list(request):
#     object_list = Post.published.all()
#     # set up pagination for all objects returned
#     # 3 posts per page
#     paginator = Paginator(object_list, 3)
#     # gets the current page number
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts=paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     # posts = Post.published.all()
#     # render function renders the list of posts into the given template
#     # render function returns an HttpResponse object with the rendered text
#     return render(request,
#                   'blog/post/list.html',
#                   { 'page': page,
#                       'posts': posts})

# POST LIST REQUEST HANDLER, CLASS VERSION
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  { 'post': post})