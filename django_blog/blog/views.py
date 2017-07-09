from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from blog.forms import EmailPostForm
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


'''
- Retrieve the post based on post_id
- Assume if the method was POST = form submission
'''
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],
                                                               cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            # django method for sending an email
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post,
                                                        'form': form,
                                                        'sent': sent})